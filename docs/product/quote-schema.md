# Quote Schema

## QuoteLineItem

- `description`: Work, material, or service described by the transcript.
- `quantity`: Numeric quantity if stated or strongly implied. Otherwise `null`.
- `unit`: Unit such as hours, items, rooms, metres, or days if stated. Otherwise `null`.
- `unit_price`: Price per unit if stated. Otherwise `null`.
- `line_total`: Total for the line item if stated or directly calculable from stated values. Otherwise `null`.

## QuoteDraft

- `customer_name`: Customer name if stated. Otherwise `null`.
- `customer_email`: Customer email if stated. Otherwise `null`.
- `customer_phone`: Customer phone number if stated. Otherwise `null`.
- `site_address`: Job site address if stated. Otherwise `null`.
- `job_title`: Short title for the job if clear from the transcript. Otherwise `null`.
- `job_summary`: Concise summary of the requested work. This is required.
- `line_items`: Work or materials that should appear on the quote.
- `subtotal`: Pre-VAT total if stated or directly calculable. Otherwise `null`.
- `vat_rate`: VAT rate if stated. Otherwise `null`.
- `vat_amount`: VAT amount if stated or directly calculable. Otherwise `null`.
- `total`: Final total if stated or directly calculable. Otherwise `null`.
- `assumptions`: Customer-facing assumptions that should be checked before sending.
- `exclusions`: Customer-facing exclusions from the quote.
- `payment_terms`: Payment terms if stated. Otherwise `null`.
- `quote_valid_days`: Validity period in days if stated. Otherwise `null`.
- `internal_notes`: Notes for the tradesperson that should not be sent directly to the customer.
- `confidence_flags`: Review warnings for uncertain or missing information.

Missing prices intentionally remain `null`. The system must not invent a quote value when the tradesperson did not state one.
