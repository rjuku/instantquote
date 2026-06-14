"""Backward-compatible audio validation helpers."""

from __future__ import annotations

from pathlib import Path

from instantquote.input_validation import (
    MAX_AUDIO_BYTES,
    SUPPORTED_AUDIO_EXTENSIONS,
    InputValidationError,
    QuoteInputKind,
    validate_quote_input,
)

__all__ = ["MAX_AUDIO_BYTES", "AudioValidationError", "validate_audio_file"]


class AudioValidationError(InputValidationError):
    """Raised when an input audio file is not suitable for transcription."""


def validate_audio_file(audio_path: Path) -> Path:
    """Validate path existence, extension, and file size."""
    try:
        validated = validate_quote_input(audio_path)
    except InputValidationError as exc:
        raise AudioValidationError(str(exc)) from exc

    if validated.kind is not QuoteInputKind.AUDIO:
        supported = ", ".join(sorted(SUPPORTED_AUDIO_EXTENSIONS))
        raise AudioValidationError(
            f"Unsupported audio extension '{validated.path.suffix}'. Supported: {supported}"
        )

    return validated.path
