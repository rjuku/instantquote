"""Audio transcription service backed by the OpenAI SDK."""

from __future__ import annotations

from pathlib import Path

from openai import OpenAI


class TranscriptionService:
    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def transcribe(self, audio_path: Path) -> str:
        """Transcribe an audio file and return plain text."""
        with audio_path.open("rb") as audio_file:
            transcript = self._client.audio.transcriptions.create(
                model=self._model,
                file=audio_file,
            )

        text = getattr(transcript, "text", None)
        if not isinstance(text, str) or not text.strip():
            raise ValueError("OpenAI returned an empty transcript.")
        return text.strip()
