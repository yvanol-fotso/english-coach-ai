from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    status_code = 500
    code = "internal"

    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message or self.code


class LLMUnavailableError(AppError):
    status_code = 503
    code = "llm_unavailable"


class LLMInvalidOutputError(AppError):
    status_code = 502
    code = "llm_bad_output"


class SpeechUnavailableError(AppError):
    status_code = 501
    code = "speech_unavailable"


class AudioTooLargeError(AppError):
    status_code = 413
    code = "audio_too_large"


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"code": exc.code, "detail": exc.message})
