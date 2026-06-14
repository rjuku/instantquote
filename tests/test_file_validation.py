from __future__ import annotations

from pathlib import Path

import pytest

from instantquote.audio_validation import (
    MAX_AUDIO_BYTES,
    AudioValidationError,
    validate_audio_file,
)


def test_validate_audio_file_accepts_supported_extension(tmp_path: Path) -> None:
    audio_path = tmp_path / "visit.m4a"
    audio_path.write_bytes(b"tiny audio placeholder")

    assert validate_audio_file(audio_path) == audio_path.resolve()


def test_validate_audio_file_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(AudioValidationError, match="does not exist"):
        validate_audio_file(tmp_path / "missing.m4a")


def test_validate_audio_file_rejects_unsupported_extension(tmp_path: Path) -> None:
    audio_path = tmp_path / "visit.txt"
    audio_path.write_text("not audio", encoding="utf-8")

    with pytest.raises(AudioValidationError, match="Unsupported audio extension"):
        validate_audio_file(audio_path)


def test_validate_audio_file_rejects_files_larger_than_25_mb(tmp_path: Path) -> None:
    audio_path = tmp_path / "large.wav"
    with audio_path.open("wb") as file:
        file.seek(MAX_AUDIO_BYTES)
        file.write(b"0")

    with pytest.raises(AudioValidationError, match="25 MB"):
        validate_audio_file(audio_path)
