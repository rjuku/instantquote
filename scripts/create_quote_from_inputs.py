"""Create a structured quote draft from one or more quote source files."""

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

from instantquote.config import load_settings
from instantquote.input_validation import InputValidationError, validate_quote_inputs
from instantquote.quote_inputs import build_quote_evidence
from instantquote.renderers.markdown_renderer import render_quote_markdown
from instantquote.services.quote_extraction_service import QuoteExtractionService
from instantquote.services.transcription_service import TranscriptionService


def _safe_stem(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return safe or "quote"


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def create_quote_from_inputs(input_paths: list[Path]) -> list[Path]:
    """Run the mixed-input quote workflow and return generated output paths."""
    if load_dotenv is not None:
        load_dotenv()

    validated_inputs = validate_quote_inputs(input_paths)
    settings = load_settings()
    settings.output_dir.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=settings.openai_api_key)
    transcription_service = TranscriptionService(client=client, model=settings.transcription_model)
    extraction_service = QuoteExtractionService(client=client, model=settings.text_model)

    evidence = build_quote_evidence(
        inputs=validated_inputs,
        transcription_service=transcription_service,
    )
    quote = extraction_service.extract(evidence)

    timestamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    base_name = f"{timestamp}-{_safe_stem(validated_inputs[0].path.stem)}"
    evidence_path = settings.output_dir / f"{base_name}.evidence.md"
    json_path = settings.output_dir / f"{base_name}.quote.json"
    markdown_path = settings.output_dir / f"{base_name}.quote.md"

    _write_text(evidence_path, evidence.render_audit_text())
    _write_text(json_path, json.dumps(quote.model_dump(mode="json"), indent=2) + "\n")
    _write_text(markdown_path, render_quote_markdown(quote))

    return [evidence_path, json_path, markdown_path]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a quote draft from audio, text, image, or mixed inputs."
    )
    parser.add_argument("input_paths", nargs="+", type=Path, help="One or more input files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        output_paths = create_quote_from_inputs(args.input_paths)
    except (InputValidationError, ValueError) as exc:
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
