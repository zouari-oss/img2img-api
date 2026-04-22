from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    image_url: str
    prompt: str
    negative_prompt: str | None = None
    strength: float | None = Field(default=None, ge=0.1, le=1.0)
    guidance_scale: float | None = Field(default=None, ge=0.0, le=20.0)
    num_inference_steps: int | None = Field(default=None, ge=1, le=100)


class GenerationResponse(BaseModel):
    status: str
    image_url: str
