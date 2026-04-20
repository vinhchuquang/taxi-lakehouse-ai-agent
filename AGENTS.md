# AGENTS.md

This repository is a graduation-project codebase for a local-first taxi data
lakehouse with a read-only AI query agent.

## Project Goal

Build an end-to-end data platform for NYC TLC taxi data that:

- ingests monthly `Yellow Taxi` and `Green Taxi` trip data
- organizes data into `Bronze -> Silver -> Gold`
- serves curated analytics from `Gold`
- exposes a read-only `Text-to-SQL` style API over curated tables

## Current Scope

Only these sources are in scope for the current phase:

- `Yellow Taxi`
- `Green Taxi`

The following are out of scope until the MVP lakehouse is stable:

- extra reference datasets unless the user explicitly reintroduces them
- `FHV`
- `HVFHV`
- streaming ingestion
- write-capable AI agents
- multi-tenant auth or production-grade access control

## Technology Decisions

Prefer these technologies unless the user explicitly changes direction:

- `Airflow` for orchestration
- `dbt` for transformations and tests
- `DuckDB` for local analytics serving
- `MinIO` for object storage
- `FastAPI` for the query API
- `OpenAI API` for the AI query layer
- `sqlglot` for SQL validation and guardrails

Do not switch the core architecture to Vanna, LangChain, LangGraph, or another
agent framework unless the user explicitly asks for that change.

## Data Modeling Rules

- Bronze stores raw source files with minimal mutation.
- Silver standardizes schema across Yellow and Green datasets.
- Gold contains curated marts for BI and AI querying.
- The AI layer must only query `Gold` tables or views.
- Prefer adding `service_type` to marts where Yellow and Green are combined.
- Keep monthly partition semantics visible in paths and pipeline manifests.
- Keep implementation focused on the two monthly TLC parquet sources only.

## Coding Priorities

When editing this repo, prioritize work in this order:

1. ingestion reliability for Yellow and Green TLC data
2. stable Bronze to Silver to Gold transforms
3. data quality checks and repeatability
4. AI query safety and schema-aware answers
5. dashboard and user-facing polish

## Guardrails For The AI Query Layer

- read-only behavior only
- no DML or DDL
- no access outside curated `Gold` objects
- validate generated SQL before execution
- apply limits to ad hoc queries
- prefer explicit semantic metadata over inferring business meaning from names

## Repo Navigation

- `airflow/dags/` contains orchestration code
- `dbt/` contains Bronze, Silver, and Gold models
- `services/api/` contains the query API
- `contracts/` contains semantic metadata for the AI layer
- `docs/` contains project context for humans and agents

## Working Style For Agents

- keep changes incremental and scoped
- do not introduce extra frameworks without clear value
- prefer local-first, testable implementations
- preserve the project narrative: lakehouse first, AI agent on top
