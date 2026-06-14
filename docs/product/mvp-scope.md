# MVP Scope

## In Scope

- CLI command that accepts a local audio file.
- File existence, extension, and size validation.
- OpenAI audio transcription.
- Raw transcript saved to disk.
- Quote extraction using schema-constrained OpenAI output.
- Pydantic validation of the extracted quote draft.
- JSON output for structured data.
- Markdown output for readable review.
- Tests for validation, models, and rendering without calling OpenAI.

## Out Of Scope

- Frontend.
- Database.
- Authentication.
- Payments or Stripe.
- AWS or other cloud deployment.
- Queues or background jobs.
- RAG or document retrieval.
- Observability tools such as Langfuse or Sentry.
- Customer management.
- Quote sending or PDF generation.
- Price books or automatic pricing.
