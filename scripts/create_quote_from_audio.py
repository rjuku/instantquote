"""Create a structured quote draft from an audio file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]

from openai import OpenAI

from instantquote.audio_validation import AudioValidationError, validate_audio_file
from instantquote.config import load_settings
from instantquote.renderers.markdown_renderer import render_quote_markdown
from instantquote.services.quote_extraction_service import QuoteExtractionService
from instantquote.services.transcription_service import TranscriptionService


def _safe_stem(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return safe or "quote"


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def create_quote_from_audio(audio_path: Path) -> list[Path]:
    """Run the full audio-to-quote workflow and return generated output paths."""
    if load_dotenv is not None:
        load_dotenv()

    validated_audio_path = validate_audio_file(audio_path)
    settings = load_settings()
    settings.output_dir.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=settings.openai_api_key)
    transcription_service = TranscriptionService(client=client, model=settings.transcription_model)
    extraction_service = QuoteExtractionService(client=client, model=settings.text_model)

    transcript = transcription_service.transcribe(validated_audio_path)
    quote = extraction_service.extract(transcript)

    timestamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    base_name = f"{timestamp}-{_safe_stem(validated_audio_path.stem)}"
    transcript_path = settings.output_dir / f"{base_name}.transcript.txt"
    json_path = settings.output_dir / f"{base_name}.quote.json"
    markdown_path = settings.output_dir / f"{base_name}.quote.md"

    _write_text(transcript_path, transcript + "\n")
    _write_text(json_path, json.dumps(quote.model_dump(mode="json"), indent=2) + "\n")
    _write_text(markdown_path, render_quote_markdown(quote))

    return [transcript_path, json_path, markdown_path]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a quote draft from an audio file.")
    parser.add_argument("audio_path", type=Path, help="Path to an audio file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        output_paths = create_quote_from_audio(args.audio_path)
    except (AudioValidationError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print("Generated files:")
    for path in output_paths:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
