"""Pydantic models for InstantQuote quote drafts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class QuoteLineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    quantity: float | None = None
    unit: str | None = None
    unit_price: float | None = None
    line_total: float | None = None


class QuoteDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_name: str | None = None
    customer_email: str | None = None
    customer_phone: str | None = None
    site_address: str | None = None
    job_title: str | None = None
    job_summary: str
    line_items: list[QuoteLineItem] = Field(default_factory=list)
    subtotal: float | None = None
    vat_rate: float | None = None
    vat_amount: float | None = None
    total: float | None = None
    assumptions: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    payment_terms: str | None = None
    quote_valid_days: int | None = None
    internal_notes: list[str] = Field(default_factory=list)
    confidence_flags: list[str] = Field(default_factory=list)
