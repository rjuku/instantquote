"""Input validation for quote source files."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

SUPPORTED_AUDIO_EXTENSIONS = {".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".wav", ".webm"}
SUPPORTED_TEXT_EXTENSIONS = {".md", ".txt"}
SUPPORTED_IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".png", ".webp"}

MAX_AUDIO_BYTES = 25 * 1024 * 1024
MAX_TEXT_BYTES = 1 * 1024 * 1024
MAX_IMAGE_BYTES = 20 * 1024 * 1024


class QuoteInputKind(StrEnum):
    AUDIO = "audio"
    TEXT = "text"
    IMAGE = "image"


@dataclass(frozen=True)
class ValidatedQuoteInput:
    path: Path
    kind: QuoteInputKind


class InputValidationError(ValueError):
    """Raised when an input file is not suitable for quote extraction."""


def classify_input_path(path: Path) -> QuoteInputKind:
    """Classify a path by supported extension."""
    suffix = path.suffix.lower()
    if suffix in SUPPORTED_AUDIO_EXTENSIONS:
        return QuoteInputKind.AUDIO
    if suffix in SUPPORTED_TEXT_EXTENSIONS:
        return QuoteInputKind.TEXT
    if suffix in SUPPORTED_IMAGE_EXTENSIONS:
        return QuoteInputKind.IMAGE

    supported = sorted(
        SUPPORTED_AUDIO_EXTENSIONS | SUPPORTED_TEXT_EXTENSIONS | SUPPORTED_IMAGE_EXTENSIONS
    )
    raise InputValidationError(
        f"Unsupported input extension '{path.suffix}'. Supported: {', '.join(supported)}"
    )


def _max_size_for_kind(kind: QuoteInputKind) -> int:
    match kind:
        case QuoteInputKind.AUDIO:
            return MAX_AUDIO_BYTES
        case QuoteInputKind.TEXT:
            return MAX_TEXT_BYTES
        case QuoteInputKind.IMAGE:
            return MAX_IMAGE_BYTES


def validate_quote_input(path: Path) -> ValidatedQuoteInput:
    """Validate path existence, extension, and file size."""
    resolved_path = path.expanduser().resolve()

    if not resolved_path.exists():
        raise InputValidationError(f"Input file does not exist: {resolved_path}")

    if not resolved_path.is_file():
        raise InputValidationError(f"Input path is not a file: {resolved_path}")

    kind = classify_input_path(resolved_path)
    max_size = _max_size_for_kind(kind)
    size_bytes = resolved_path.stat().st_size
    if size_bytes > max_size:
        limit_mb = max_size // (1024 * 1024)
        raise InputValidationError(
            f"{kind.value.title()} file is larger than the {limit_mb} MB limit."
        )

    return ValidatedQuoteInput(path=resolved_path, kind=kind)


def validate_quote_inputs(paths: list[Path]) -> list[ValidatedQuoteInput]:
    """Validate one or more quote source files."""
    if not paths:
        raise InputValidationError("At least one input file is required.")

    return [validate_quote_input(path) for path in paths]
