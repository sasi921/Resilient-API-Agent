# Resilient API Agent

A practical Python agent that treats unreliable APIs as a normal engineering condition instead of an exceptional surprise.

It wraps HTTP JSON tools with **timeouts, retry budgets, exponential backoff, structured attempt history, and graceful degradation** so downstream AI systems can make decisions using trustworthy tool observations.

## Why this project matters

AI agents increasingly depend on external APIs. Those APIs can be slow, rate-limited, temporarily unavailable, or return invalid payloads. A production-grade agent should not fabricate an answer when a tool fails.

## Architecture

`Request → API tool → timeout/retry policy → exponential backoff → structured observation → healthy/degraded response`

Retryable HTTP responses: `408`, `429`, `500`, `502`, `503`, and `504`.

## Features

- Explicit request timeouts
- Configurable retry budget
- Exponential backoff
- Retryable status-code policy
- Structured Pydantic tool results
- Attempt-level status/error history
- Graceful degraded-state response
- JSON payload preview
- No API key required for the default demo
- Automated tests with mocked HTTP behavior

## Quick start

```bash
git clone https://github.com/sasi921/Resilient-API-Agent.git
cd Resilient-API-Agent

python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt

python app.py
python app.py https://jsonplaceholder.typicode.com/users/1
pytest -q
```

## Concepts to study

Transient vs. permanent failures, request timeouts, retry budgets, exponential backoff, rate limiting, structured tool errors, graceful degradation, observability of tool execution, and why agent systems should never hide tool failure.

## Extension ideas

Add jitter to the retry schedule, implement a circuit breaker, add per-host retry budgets, and record latency/error metrics for observability.

## Portfolio note

This project is part of the **AI Agent Engineering Lab**, a practical collection of standalone AI-agent projects progressing from core tool use to RAG, memory, planning, MCP, multi-agent systems, evaluation, and production architecture.
