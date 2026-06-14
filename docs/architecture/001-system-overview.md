# System Overview

InstantQuote Phase 1 is a command-line vertical slice. It accepts an audio file and produces three local output files: a transcript, a validated JSON quote draft, and a readable Markdown quote draft.

## Request Flow

1. The user runs `python scripts/create_quote_from_audio.py path/to/audio.m4a`.
2. The CLI validates that the path exists, is a file, uses a supported extension, and is no larger than 25 MB.
3. Runtime settings are loaded from environment variables.
4. `TranscriptionService` sends the audio file to the OpenAI transcription endpoint.
5. The raw transcript is held in memory and later written to disk.
6. `QuoteExtractionService` sends the transcript to the OpenAI Responses API with schema-constrained output.
7. The parsed response is validated as a Pydantic `QuoteDraft`.
8. The CLI writes transcript text, JSON, and Markdown files to `output/`.
9. The generated paths are printed for the user.

The services isolate external calls so tests can avoid the real OpenAI API.
