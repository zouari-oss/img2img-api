from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.generation import router as generation_router

app = FastAPI(
    title="img2img-api",
    description="Generate images from input images + prompts using Stable Diffusion (Anything V5)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation_router, prefix="/api", tags=["Generation"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "img2img-api is running", "docs": "/docs"}
