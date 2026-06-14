from __future__ import annotations

from pathlib import Path

import pytest

from instantquote.input_validation import (
    MAX_IMAGE_BYTES,
    MAX_TEXT_BYTES,
    InputValidationError,
    QuoteInputKind,
    validate_quote_input,
    validate_quote_inputs,
)


def test_validate_quote_input_accepts_text_file(tmp_path: Path) -> None:
    text_path = tmp_path / "job.txt"
    text_path.write_text("Replace tap. Price is 120.", encoding="utf-8")

    validated = validate_quote_input(text_path)

    assert validated.path == text_path.resolve()
    assert validated.kind is QuoteInputKind.TEXT


def test_validate_quote_input_accepts_image_file(tmp_path: Path) -> None:
    image_path = tmp_path / "sink.jpg"
    image_path.write_bytes(b"not a real image but enough for validation")

    validated = validate_quote_input(image_path)

    assert validated.path == image_path.resolve()
    assert validated.kind is QuoteInputKind.IMAGE


def test_validate_quote_inputs_requires_at_least_one_path() -> None:
    with pytest.raises(InputValidationError, match="At least one input file"):
        validate_quote_inputs([])


def test_validate_quote_input_rejects_large_text_file(tmp_path: Path) -> None:
    text_path = tmp_path / "large.txt"
    with text_path.open("wb") as file:
        file.seek(MAX_TEXT_BYTES)
        file.write(b"0")

    with pytest.raises(InputValidationError, match="1 MB"):
        validate_quote_input(text_path)


def test_validate_quote_input_rejects_large_image_file(tmp_path: Path) -> None:
    image_path = tmp_path / "large.png"
    with image_path.open("wb") as file:
        file.seek(MAX_IMAGE_BYTES)
        file.write(b"0")

    with pytest.raises(InputValidationError, match="20 MB"):
        validate_quote_input(image_path)
