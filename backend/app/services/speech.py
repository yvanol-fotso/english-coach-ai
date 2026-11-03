import asyncio
import importlib.util
import sys
import tempfile
from pathlib import Path

from app.core.config import Settings
from app.core.errors import SpeechUnavailableError


class SpeechService:
    def __init__(self, settings: Settings) -> None:
        self._cfg = settings
        self._whisper = None
        self._lock = asyncio.Lock()

    @property
    def stt_available(self) -> bool:
        return importlib.util.find_spec("faster_whisper") is not None

    @property
    def tts_available(self) -> bool:
        has_piper = importlib.util.find_spec("piper") is not None
        return has_piper and Path(self._cfg.piper_voice_path).is_file()

    def _load_whisper(self, force_cpu: bool):
        from faster_whisper import WhisperModel

        if force_cpu:
            return WhisperModel(self._cfg.whisper_model, device="cpu", compute_type="int8")
        try:
            return WhisperModel(
                self._cfg.whisper_model,
                device=self._cfg.whisper_device,
                compute_type=self._cfg.whisper_compute_type,
            )
        except Exception:
            return WhisperModel(self._cfg.whisper_model, device="cpu", compute_type="int8")

    def _transcribe_sync(self, path: str, language: str) -> str:
        for attempt in (0, 1):
            if self._whisper is None:
                self._whisper = self._load_whisper(force_cpu=attempt == 1)
            try:
                segments, _ = self._whisper.transcribe(path, language=language, vad_filter=True, beam_size=1)
                return " ".join(s.text.strip() for s in segments).strip()
            except RuntimeError:
                if attempt == 1:
                    raise
                self._whisper = None
        return ""

    async def transcribe(self, audio: bytes, language: str) -> str:
        if not self.stt_available:
            raise SpeechUnavailableError("Whisper is not installed: pip install -r requirements-speech.txt")
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(audio)
        try:
            async with self._lock:
                return await asyncio.to_thread(self._transcribe_sync, tmp.name, language)
        except RuntimeError as exc:
            raise SpeechUnavailableError("Whisper transcription failed.") from exc
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    async def synthesize(self, text: str) -> bytes:
        if not self.tts_available:
            raise SpeechUnavailableError("Piper or its English voice is missing (see backend/README.md).")
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "speech.wav"
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "piper", "-m", self._cfg.piper_voice_path, "-f", str(out),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.communicate(text.encode())
            if proc.returncode != 0 or not out.exists():
                raise SpeechUnavailableError("Piper synthesis failed.")
            return out.read_bytes()
