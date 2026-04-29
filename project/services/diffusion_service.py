import base64
import io
import os

import requests
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

from core.config import settings


class DiffusionService:
    def __init__(self):
        self.pipe = None
        self.backend = None

        if os.path.isfile(settings.MODEL_PATH):
            self.pipe = StableDiffusionImg2ImgPipeline.from_single_file(
                settings.MODEL_PATH,
                torch_dtype=torch.float16 if settings.DEVICE == "cuda" else torch.float32,
            ).to(settings.DEVICE)
            self.pipe.enable_attention_slicing()
            if settings.DEVICE == "cuda":
                self.pipe.enable_vae_tiling()
            self.backend = "local"
        elif settings.HF_MODEL_ID:
            self.backend = "huggingface"
        else:
            raise RuntimeError(
                "No local model found and no Hugging Face model configured. "
                "Set MODEL_PATH to an existing file or set HF_MODEL_ID."
            )

    def generate(
        self,
        image,
        prompt,
        negative_prompt=None,
        strength=None,
        guidance_scale=None,
        num_inference_steps=None,
    ):
        resolved_strength = float(strength if strength is not None else settings.DEFAULT_STRENGTH)
        resolved_guidance = float(
            guidance_scale if guidance_scale is not None else settings.DEFAULT_GUIDANCE_SCALE
        )
        resolved_steps = int(
            num_inference_steps
            if num_inference_steps is not None
            else settings.DEFAULT_NUM_INFERENCE_STEPS
        )
        resolved_steps = max(settings.MIN_INFERENCE_STEPS, min(settings.MAX_INFERENCE_STEPS, resolved_steps))

        if self.backend == "local":
            result = self.pipe(
                prompt=prompt,
                image=image,
                strength=resolved_strength,
                guidance_scale=resolved_guidance,
                num_inference_steps=resolved_steps,
                negative_prompt=negative_prompt or "",
            ).images[0]
            return result

        return self._generate_with_huggingface(
            image=image,
            prompt=prompt,
            negative_prompt=negative_prompt,
            strength=resolved_strength,
            guidance_scale=resolved_guidance,
            num_inference_steps=resolved_steps,
        )

    def _generate_with_huggingface(
        self,
        image: Image.Image,
        prompt: str,
        negative_prompt: str | None,
        strength: float,
        guidance_scale: float,
        num_inference_steps: int,
    ) -> Image.Image:
        model_id = settings.HF_MODEL_ID
        if not model_id:
            raise RuntimeError("HF_MODEL_ID is required when local model is not available.")

        endpoint = settings.HF_API_URL or f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Accept": "image/png"}
        if settings.HF_API_TOKEN:
            headers["Authorization"] = f"Bearer {settings.HF_API_TOKEN}"

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        image_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        payload = {
            "inputs": prompt,
            "parameters": {
                "image": image_b64,
                "strength": strength,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
                "negative_prompt": negative_prompt or "",
            },
            "options": {
                "wait_for_model": settings.HF_WAIT_FOR_MODEL,
            },
        }

        resp = requests.post(endpoint, headers=headers, json=payload, timeout=settings.HF_TIMEOUT)
        if not resp.ok:
            raise RuntimeError(f"Hugging Face inference failed ({resp.status_code}): {resp.text}")

        content_type = resp.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            raise RuntimeError(
                "Hugging Face inference returned a non-image response: "
                f"{resp.text}"
            )

        return Image.open(io.BytesIO(resp.content)).convert("RGB")


diffusion_service = DiffusionService()
