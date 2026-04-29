import os
from dotenv import load_dotenv

load_dotenv()


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    MODEL_PATH = os.getenv("MODEL_PATH")
    DEVICE = os.getenv("DEVICE", "cuda")
    BASE_URL = os.getenv("BASE_URL")
    FREEIMAGE_API_KEY = os.getenv("FREEIMAGE_API_KEY")
    FREEIMAGE_UPLOAD_URL = os.getenv("FREEIMAGE_UPLOAD_URL")
    HF_MODEL_ID = os.getenv("HF_MODEL_ID")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN")
    HF_API_URL = os.getenv("HF_API_URL")
    HF_TIMEOUT = int(os.getenv("HF_TIMEOUT", "120"))
    HF_WAIT_FOR_MODEL = _env_bool("HF_WAIT_FOR_MODEL", default=True)
    DEFAULT_STRENGTH = float(os.getenv("DEFAULT_STRENGTH", "0.55"))
    DEFAULT_GUIDANCE_SCALE = float(os.getenv("DEFAULT_GUIDANCE_SCALE", "5.0"))
    DEFAULT_NUM_INFERENCE_STEPS = int(os.getenv("DEFAULT_NUM_INFERENCE_STEPS", "4"))
    MIN_INFERENCE_STEPS = int(os.getenv("MIN_INFERENCE_STEPS", "1"))
    MAX_INFERENCE_STEPS = int(os.getenv("MAX_INFERENCE_STEPS", "30"))


settings = Settings()
