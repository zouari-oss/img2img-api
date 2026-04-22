import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL_PATH = os.getenv("MODEL_PATH", "models/anything-v5.safetensors")
    DEVICE = os.getenv("DEVICE", "cuda")
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")  # change in prod
    FREEIMAGE_API_KEY = os.getenv("FREEIMAGE_API_KEY")
    FREEIMAGE_UPLOAD_URL = os.getenv("FREEIMAGE_UPLOAD_URL", "https://freeimage.host/api/1/upload")
    DEFAULT_STRENGTH = float(os.getenv("DEFAULT_STRENGTH", "0.55"))
    DEFAULT_GUIDANCE_SCALE = float(os.getenv("DEFAULT_GUIDANCE_SCALE", "5.0"))
    DEFAULT_NUM_INFERENCE_STEPS = int(os.getenv("DEFAULT_NUM_INFERENCE_STEPS", "4"))
    MIN_INFERENCE_STEPS = int(os.getenv("MIN_INFERENCE_STEPS", "1"))
    MAX_INFERENCE_STEPS = int(os.getenv("MAX_INFERENCE_STEPS", "30"))


settings = Settings()
