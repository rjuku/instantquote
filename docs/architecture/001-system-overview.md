# System Overview

InstantQuote Phase 1 is a command-line vertical slice. It accepts one or more local input files and produces three local output files: an evidence audit, a validated JSON quote draft, and a readable Markdown quote draft.

The product direction is WhatsApp-first. In production, the bot will collect voice notes, text notes, and photos into a quote session. It should wait until the user writes `generate`, then send the collected evidence to this backend workflow. Quote review and correction happens in WhatsApp, not in a browser-based quote editor.

## Request Flow

1. The user runs `python scripts/create_quote_from_inputs.py path/to/audio.m4a path/to/note.txt path/to/photo.jpg`.
2. The CLI validates that each path exists, is a file, uses a supported extension, and stays within the size limit for its type.
3. Runtime settings are loaded from environment variables.
4. `TranscriptionService` sends each audio file to the OpenAI transcription endpoint.
5. Text files are read as UTF-8.
6. Image files are encoded as data URLs and sent as image evidence.
7. The collected evidence audit is held in memory and later written to disk.
8. `QuoteExtractionService` sends the evidence to the OpenAI Responses API with schema-constrained output.
9. The parsed response is validated as a Pydantic `QuoteDraft`.
10. The CLI writes evidence Markdown, quote JSON, and quote Markdown files to `output/`.
11. The generated paths are printed for the user.

The services isolate external calls so tests can avoid the real OpenAI API.
