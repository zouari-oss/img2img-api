import requests
from PIL import Image
from io import BytesIO


def download_image(url: str) -> Image.Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img.resize((512, 512))
