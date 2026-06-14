"""Create a structured quote draft from one audio file.

This wrapper is kept for compatibility. New work should use
`scripts/create_quote_from_inputs.py`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from instantquote.audio_validation import AudioValidationError, validate_audio_file
from scripts.create_quote_from_inputs import create_quote_from_inputs


def create_quote_from_audio(audio_path: Path) -> list[Path]:
    """Run the full audio-to-quote workflow and return generated output paths."""
    validated_audio_path = validate_audio_file(audio_path)
    return create_quote_from_inputs([validated_audio_path])


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
