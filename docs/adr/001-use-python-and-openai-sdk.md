# ADR 001: Use Python And The Official OpenAI SDK

## Status

Accepted

## Context

The first product risk is whether a voice note can become a useful quote draft with a small, testable codebase. Python has strong support for CLI tooling, Pydantic validation, and the official OpenAI SDK.

## Decision

Use Python 3.12, uv, the official OpenAI Python SDK, Pydantic v2, pytest, ruff, and mypy.

## Consequences

The code stays simple and easy to run locally. The OpenAI SDK provides maintained API bindings, while Pydantic gives a clear application data contract. Future phases can add a web API or database without replacing the core quote extraction model.
