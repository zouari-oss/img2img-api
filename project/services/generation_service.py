import io
import requests
from utils.downloader import download_image
from services.diffusion_service import diffusion_service
from core.config import settings


def _find_first_url(obj):
    if isinstance(obj, str):
        if obj.startswith("http://") or obj.startswith("https://"):
            return obj
        return None
    if isinstance(obj, dict):
        for v in obj.values():
            res = _find_first_url(v)
            if res:
                return res
    if isinstance(obj, list):
        for v in obj:
            res = _find_first_url(v)
            if res:
                return res
    return None


class GenerationService:
    @staticmethod
    def generate(image_url: str, prompt: str, negative_prompt: str | None):

        # 1. download input
        image = download_image(image_url)

        # 2. generate
        output = diffusion_service.generate(image, prompt, negative_prompt)

        # 3. upload to freeimage.host only
        api_key = settings.FREEIMAGE_API_KEY
        upload_url = settings.FREEIMAGE_UPLOAD_URL

        if not api_key:
            raise RuntimeError("FREEIMAGE_API_KEY is not configured; refusing to save output locally.")

        buf = io.BytesIO()
        output.save(buf, format="PNG")
        buf.seek(0)

        files = {"source": ("image.png", buf, "image/png")}
        data = {"key": api_key, "format": "json", "action": "upload"}

        resp = requests.post(upload_url, files=files, data=data, timeout=30)
        resp.raise_for_status()
        j = resp.json()
        hosted = _find_first_url(j)
        if not hosted:
            raise RuntimeError(f"Upload succeeded but no hosted URL found in response: {j}")

        return hosted
