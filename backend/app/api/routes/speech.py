from typing import Annotated

from fastapi import APIRouter, Form, Response, UploadFile

from app.api.deps import Config, Speech
from app.core.errors import AudioTooLargeError
from app.schemas.speech import SynthesizeRequest

router = APIRouter(prefix="/speech", tags=["speech"])


@router.post("/transcribe")
async def transcribe(
    speech: Speech,
    cfg: Config,
    file: UploadFile,
    language: Annotated[str, Form(pattern=r"^[a-z]{2}$")] = "en",
) -> dict:
    audio = await file.read(cfg.max_audio_bytes + 1)
    if len(audio) > cfg.max_audio_bytes:
        raise AudioTooLargeError()
    return {"text": await speech.transcribe(audio, language)}


@router.post("/synthesize")
async def synthesize(body: SynthesizeRequest, speech: Speech) -> Response:
    return Response(await speech.synthesize(body.text), media_type="audio/wav")
