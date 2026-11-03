from fastapi import APIRouter

from app.api.deps import LLM, Config, Speech

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(llm: LLM, cfg: Config, speech: Speech) -> dict:
    models = await llm.installed_models()
    return {
        "api": True,
        "ollama": bool(models),
        "model": cfg.ollama_model,
        "model_ready": cfg.ollama_model in models,
        "stt": speech.stt_available,
        "tts": speech.tts_available,
    }
