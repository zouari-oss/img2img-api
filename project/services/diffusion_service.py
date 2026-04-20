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

    def generate(self, image, prompt, negative_prompt=None):
        result = self.pipe(
            prompt=prompt,
            image=image,
            strength=0.6,
            guidance_scale=7,
            num_inference_steps=25,
            negative_prompt=negative_prompt or "",
        ).images[0]

        return result


diffusion_service = DiffusionService()
