"""Build model-ready quote context from mixed input files."""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from instantquote.input_validation import QuoteInputKind, ValidatedQuoteInput


@dataclass(frozen=True)
class TextEvidence:
    label: str
    content: str


@dataclass(frozen=True)
class ImageEvidence:
    label: str
    path: Path
    media_type: str
    data_url: str


@dataclass(frozen=True)
class QuoteEvidenceBundle:
    text_items: list[TextEvidence] = field(default_factory=list)
    image_items: list[ImageEvidence] = field(default_factory=list)

    def render_audit_text(self) -> str:
        """Render a human-readable record of the evidence sent for extraction."""
        sections: list[str] = []
        for text_item in self.text_items:
            sections.append(f"## {text_item.label}\n\n{text_item.content.strip()}")
        for image_item in self.image_items:
            sections.append(f"## {image_item.label}\n\nImage file: {image_item.path}")
        return "\n\n".join(sections).strip() + "\n"


class SupportsTranscription(Protocol):
    def transcribe(self, audio_path: Path) -> str:
        """Return a transcript for an audio file."""


def _media_type_for_image(path: Path) -> str:
    match path.suffix.lower():
        case ".jpg" | ".jpeg":
            return "image/jpeg"
        case ".png":
            return "image/png"
        case ".webp":
            return "image/webp"
        case _:
            raise ValueError(f"Unsupported image extension: {path.suffix}")


def _image_to_data_url(path: Path) -> tuple[str, str]:
    media_type = _media_type_for_image(path)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return media_type, f"data:{media_type};base64,{encoded}"


def build_quote_evidence(
    inputs: list[ValidatedQuoteInput],
    transcription_service: SupportsTranscription,
) -> QuoteEvidenceBundle:
    """Convert validated files into text and image evidence for quote extraction."""
    text_items: list[TextEvidence] = []
    image_items: list[ImageEvidence] = []

    for index, item in enumerate(inputs, start=1):
        label = f"Input {index}: {item.path.name}"
        match item.kind:
            case QuoteInputKind.AUDIO:
                transcript = transcription_service.transcribe(item.path)
                text_items.append(TextEvidence(label=f"{label} transcript", content=transcript))
            case QuoteInputKind.TEXT:
                content = item.path.read_text(encoding="utf-8").strip()
                text_items.append(TextEvidence(label=f"{label} text", content=content))
            case QuoteInputKind.IMAGE:
                media_type, data_url = _image_to_data_url(item.path)
                image_items.append(
                    ImageEvidence(
                        label=f"{label} image",
                        path=item.path,
                        media_type=media_type,
                        data_url=data_url,
                    )
                )

    return QuoteEvidenceBundle(text_items=text_items, image_items=image_items)
