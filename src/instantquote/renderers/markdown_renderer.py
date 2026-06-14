"""Markdown rendering for quote drafts."""

from __future__ import annotations

from instantquote.models import QuoteDraft, QuoteLineItem


def _value(value: object) -> str:
    if value is None:
        return "Not provided"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _money(value: float | None) -> str:
    if value is None:
        return "Not provided"
    return f"GBP {value:.2f}"


def _render_line_item(index: int, item: QuoteLineItem) -> str:
    return (
        f"| {index} | {item.description} | {_value(item.quantity)} | "
        f"{_value(item.unit)} | {_money(item.unit_price)} | {_money(item.line_total)} |"
    )


def render_quote_markdown(quote: QuoteDraft) -> str:
    """Render a QuoteDraft as customer-readable Markdown."""
    lines = [
        f"# {_value(quote.job_title)}",
        "",
        "## Customer",
        f"- Name: {_value(quote.customer_name)}",
        f"- Email: {_value(quote.customer_email)}",
        f"- Phone: {_value(quote.customer_phone)}",
        f"- Site address: {_value(quote.site_address)}",
        "",
        "## Job Summary",
        quote.job_summary,
        "",
        "## Line Items",
        "| # | Description | Quantity | Unit | Unit Price | Line Total |",
        "|---|---|---:|---|---:|---:|",
    ]

    if quote.line_items:
        lines.extend(
            _render_line_item(index, item)
            for index, item in enumerate(quote.line_items, start=1)
        )
    else:
        lines.append(
            "| 1 | No line items provided | Not provided | "
            "Not provided | Not provided | Not provided |"
        )

    lines.extend(
        [
            "",
            "## Totals",
            f"- Subtotal: {_money(quote.subtotal)}",
            f"- VAT rate: {_value(quote.vat_rate)}",
            f"- VAT amount: {_money(quote.vat_amount)}",
            f"- Total: {_money(quote.total)}",
            "",
            "## Assumptions",
        ]
    )
    lines.extend(f"- {item}" for item in quote.assumptions) if quote.assumptions else lines.append(
        "- None provided"
    )

    lines.append("")
    lines.append("## Exclusions")
    lines.extend(f"- {item}" for item in quote.exclusions) if quote.exclusions else lines.append(
        "- None provided"
    )

    lines.extend(
        [
            "",
            "## Payment Terms",
            _value(quote.payment_terms),
            "",
            "## Validity",
            f"{_value(quote.quote_valid_days)} days",
            "",
            "## Review Flags",
        ]
    )
    lines.extend(
        f"- {item}" for item in quote.confidence_flags
    ) if quote.confidence_flags else lines.append("- None")

    lines.extend(["", "## Internal Notes"])
    lines.extend(
        f"- {item}" for item in quote.internal_notes
    ) if quote.internal_notes else lines.append("- None")

    return "\n".join(lines) + "\n"
