from pydantic import BaseModel


class GenerationRequest(BaseModel):
    image_url: str
    prompt: str
    negative_prompt: str | None = None


class GenerationResponse(BaseModel):
    status: str
    image_url: str
