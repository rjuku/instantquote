from __future__ import annotations

import json
from pathlib import Path

from instantquote.models import QuoteDraft


def test_quote_draft_fixture_validates() -> None:
    fixture_path = Path("tests/fixtures/sample_quote_draft.json")
    quote = QuoteDraft.model_validate_json(fixture_path.read_text(encoding="utf-8"))

    assert quote.customer_name == "Sarah Jones"
    assert quote.line_items[0].quantity == 2.0
    assert quote.line_items[0].unit_price is None


def test_quote_draft_rejects_unknown_fields() -> None:
    payload = {
        "job_summary": "Replace a leaking tap.",
        "line_items": [],
        "assumptions": [],
        "exclusions": [],
        "internal_notes": [],
        "confidence_flags": [],
        "made_up_field": "not allowed",
    }

    try:
        QuoteDraft.model_validate(payload)
    except ValueError as exc:
        assert "made_up_field" in str(exc)
    else:
        raise AssertionError("QuoteDraft accepted an unknown field.")


def test_expected_fixture_keeps_missing_prices_null() -> None:
    fixture_path = Path("tests/fixtures/sample_quote_draft.json")
    data = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert data["subtotal"] is None
    assert data["total"] is None
    assert data["line_items"][0]["unit_price"] is None
