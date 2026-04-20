import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL_PATH = os.getenv("MODEL_PATH", "models/anything-v5.safetensors")
    DEVICE = os.getenv("DEVICE", "cuda")
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")  # change in prod
    FREEIMAGE_API_KEY = os.getenv("FREEIMAGE_API_KEY")
    FREEIMAGE_UPLOAD_URL = os.getenv("FREEIMAGE_UPLOAD_URL", "https://freeimage.host/api/1/upload")


settings = Settings()
