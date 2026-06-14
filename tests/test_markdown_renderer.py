from __future__ import annotations

from instantquote.models import QuoteDraft, QuoteLineItem
from instantquote.renderers.markdown_renderer import render_quote_markdown


def test_markdown_renderer_handles_missing_values() -> None:
    quote = QuoteDraft(
        customer_name=None,
        customer_email=None,
        customer_phone=None,
        site_address=None,
        job_title=None,
        job_summary="Replace a leaking kitchen tap.",
        line_items=[
            QuoteLineItem(
                description="Replacement tap",
                quantity=None,
                unit=None,
                unit_price=None,
                line_total=None,
            )
        ],
        subtotal=None,
        vat_rate=None,
        vat_amount=None,
        total=None,
        assumptions=[],
        exclusions=[],
        payment_terms=None,
        quote_valid_days=None,
        internal_notes=["Confirm tap cost."],
        confidence_flags=["No price was stated."],
    )

    markdown = render_quote_markdown(quote)

    assert "# Not provided" in markdown
    assert "GBP" not in markdown
    assert "Not provided" in markdown
    assert "No price was stated." in markdown
