# Python API Integration Notes

## API Keys

The OpenAI SDK reads credentials from the application configuration. Store `OPENAI_API_KEY` in a local `.env` file or shell environment. Do not commit real keys.

## Environment Variables

InstantQuote uses environment variables for settings that may change between machines:

- `OPENAI_API_KEY`: required OpenAI credential.
- `INSTANTQUOTE_TRANSCRIPTION_MODEL`: transcription model, defaulting to `gpt-4o-mini-transcribe`.
- `INSTANTQUOTE_TEXT_MODEL`: required quote extraction model.
- `INSTANTQUOTE_OUTPUT_DIR`: output folder, defaulting to `output`.

## Transcription

The transcription service opens the audio file in binary mode and sends it to the OpenAI transcription endpoint. The CLI validates file type and size first so unsupported inputs fail before an API call.

## Structured Extraction

The quote extraction service sends the transcript to the OpenAI Responses API and asks for output matching the `QuoteDraft` Pydantic schema. The transcript is treated as untrusted job content, so any instructions inside it are not allowed to override extraction rules.

## Pydantic Validation

Pydantic v2 validates the model output before files are written. Unknown fields are rejected, required fields must exist, and missing optional details remain `null`.

## Common Failure Modes

- Missing `OPENAI_API_KEY`.
- Missing `INSTANTQUOTE_TEXT_MODEL`.
- Unsupported audio extension.
- Audio file larger than 25 MB.
- Empty transcript returned by the transcription endpoint.
- Model output that does not satisfy the quote schema.
- Network or API errors from OpenAI.

## Lessons Learned

Keep external calls behind small service classes. Validate files before making network calls. Treat all voice transcript text as data, not instructions. Prefer explicit `null` values over invented prices or customer details.
