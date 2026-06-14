from __future__ import annotations

from pathlib import Path

from instantquote.input_validation import QuoteInputKind, ValidatedQuoteInput
from instantquote.quote_inputs import build_quote_evidence


class FakeTranscriptionService:
    def transcribe(self, audio_path: Path) -> str:
        return f"Transcript for {audio_path.name}"


def test_build_quote_evidence_combines_multiple_audio_and_text(tmp_path: Path) -> None:
    first_audio = tmp_path / "one.m4a"
    second_audio = tmp_path / "two.m4a"
    text_path = tmp_path / "notes.txt"
    first_audio.write_bytes(b"audio")
    second_audio.write_bytes(b"audio")
    text_path.write_text("Customer said total should be 240.", encoding="utf-8")

    evidence = build_quote_evidence(
        inputs=[
            ValidatedQuoteInput(path=first_audio, kind=QuoteInputKind.AUDIO),
            ValidatedQuoteInput(path=second_audio, kind=QuoteInputKind.AUDIO),
            ValidatedQuoteInput(path=text_path, kind=QuoteInputKind.TEXT),
        ],
        transcription_service=FakeTranscriptionService(),
    )

    audit_text = evidence.render_audit_text()

    assert len(evidence.text_items) == 3
    assert "Transcript for one.m4a" in audit_text
    assert "Transcript for two.m4a" in audit_text
    assert "Customer said total should be 240." in audit_text


def test_build_quote_evidence_encodes_image_as_data_url(tmp_path: Path) -> None:
    image_path = tmp_path / "damage.png"
    image_path.write_bytes(b"image bytes")

    evidence = build_quote_evidence(
        inputs=[ValidatedQuoteInput(path=image_path, kind=QuoteInputKind.IMAGE)],
        transcription_service=FakeTranscriptionService(),
    )

    assert len(evidence.image_items) == 1
    assert evidence.image_items[0].media_type == "image/png"
    assert evidence.image_items[0].data_url.startswith("data:image/png;base64,")
