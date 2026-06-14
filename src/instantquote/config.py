"""Runtime configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"
DEFAULT_OUTPUT_DIR = Path("output")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    transcription_model: str
    text_model: str
    output_dir: Path


def load_settings() -> Settings:
    """Load settings from environment variables and fail early for required values."""
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    text_model = os.getenv("INSTANTQUOTE_TEXT_MODEL", "").strip()

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is required. Add it to your environment or .env file.")

    if not text_model:
        raise ValueError(
            "INSTANTQUOTE_TEXT_MODEL is required. Add it to your environment or .env file."
        )

    return Settings(
        openai_api_key=openai_api_key,
        transcription_model=os.getenv(
            "INSTANTQUOTE_TRANSCRIPTION_MODEL",
            DEFAULT_TRANSCRIPTION_MODEL,
        ).strip()
        or DEFAULT_TRANSCRIPTION_MODEL,
        text_model=text_model,
        output_dir=Path(os.getenv("INSTANTQUOTE_OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR))),
    )
