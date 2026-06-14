# ADR 002: Use Structured Outputs

## Status

Accepted

## Context

Quote drafts contain money, customer details, review flags, and internal notes. Parsing arbitrary model text would be fragile and could silently lose or misplace important fields.

## Decision

Use OpenAI Structured Outputs with the Pydantic `QuoteDraft` schema, then validate the parsed result again in application code.

## Why This Is Safer

Schema-constrained output makes the model return data shaped like the application contract instead of free-form prose. This reduces brittle string parsing, makes missing values explicit as `null`, rejects unexpected fields, and gives tests a stable contract.

Structured output does not remove the need for human review. The extraction instructions still require confidence flags for uncertain information, and the final quote remains a draft.
