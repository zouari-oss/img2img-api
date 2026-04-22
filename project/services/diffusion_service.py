import torch
from diffusers import StableDiffusionImg2ImgPipeline
from core.config import settings


class DiffusionService:
    def __init__(self):
        self.pipe = StableDiffusionImg2ImgPipeline.from_single_file(
            settings.MODEL_PATH,
            torch_dtype=torch.float16 if settings.DEVICE == "cuda" else torch.float32,
        ).to(settings.DEVICE)

        self.pipe.enable_attention_slicing()
        if settings.DEVICE == "cuda":
            self.pipe.enable_vae_tiling()

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

        result = self.pipe(
            prompt=prompt,
            image=image,
            strength=resolved_strength,
            guidance_scale=resolved_guidance,
            num_inference_steps=resolved_steps,
            negative_prompt=negative_prompt or "",
        ).images[0]

        return result


diffusion_service = DiffusionService()
