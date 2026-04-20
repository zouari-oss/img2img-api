from fastapi import APIRouter
from schemas.generation_schema import GenerationRequest, GenerationResponse
from services.generation_service import GenerationService

router = APIRouter()


@router.post("/generate", response_model=GenerationResponse)
def generate_image(req: GenerationRequest):

    image_url = GenerationService.generate(
        req.image_url, req.prompt, req.negative_prompt
    )

    return {"status": "success", "image_url": image_url}
