"""Audio input validation for the CLI workflow."""

from __future__ import annotations

from pathlib import Path

SUPPORTED_AUDIO_EXTENSIONS = {".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".wav", ".webm"}
MAX_AUDIO_BYTES = 25 * 1024 * 1024


class AudioValidationError(ValueError):
    """Raised when an input audio file is not suitable for transcription."""


def validate_audio_file(audio_path: Path) -> Path:
    """Validate path existence, extension, and file size."""
    resolved_path = audio_path.expanduser().resolve()

    if not resolved_path.exists():
        raise AudioValidationError(f"Audio file does not exist: {resolved_path}")

    if not resolved_path.is_file():
        raise AudioValidationError(f"Audio path is not a file: {resolved_path}")

    if resolved_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_AUDIO_EXTENSIONS))
        raise AudioValidationError(
            f"Unsupported audio extension '{resolved_path.suffix}'. Supported: {supported}"
        )

    size_bytes = resolved_path.stat().st_size
    if size_bytes > MAX_AUDIO_BYTES:
        raise AudioValidationError("Audio file is larger than the 25 MB limit.")

    return resolved_path
