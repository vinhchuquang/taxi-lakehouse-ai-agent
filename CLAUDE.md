# CLAUDE.md

Taxi lakehouse graduation project — NYC TLC data, Bronze→Silver→Gold, read-only AI query agent.
See AGENTS.md for full scope, tech decisions, and data modeling rules.

> **Đang viết/sửa BÁO CÁO tốt nghiệp (LaTeX)?** Đọc trước:
> [`docs/cai-thien-bao-cao/HANDOFF.md`](docs/cai-thien-bao-cao/HANDOFF.md) (trạng thái + số liệu đã kiểm chứng + việc còn lại)
> và [`Đồ_án_TN_ChuQuangVinh_official/CLAUDE.md`](Đồ_án_TN_ChuQuangVinh_official/CLAUDE.md) (quy tắc viết báo cáo).
> Các quy tắc *code* dưới đây KHÔNG áp dụng cho việc viết báo cáo.

## Quick Start

```bash
docker compose up -d          # start full stack
docker compose up -d --build  # only after Dockerfile/requirements changes
python -m pytest -p no:cacheprovider  # unit tests (host)
```

## Do Not

- Switch orchestration away from Airflow/dbt/DuckDB/MinIO/FastAPI without explicit instruction
- Install runtime deps (`sqlglot`, `duckdb`) into host Python — use the `api` container
- Add FHV, HVFHV, streaming ingestion, or write-capable agent features
- Run `docker compose up -d --build` unless an image dependency actually changed
- Expose any non-Gold table to the agent without updating `contracts/semantic_catalog.yaml`

## Verification Cheatsheet

| Changed area | Command |
|---|---|
| Python/unit | `python -m pytest -p no:cacheprovider` |
| dbt models | run `dbt build` inside Airflow scheduler container (see `docs/runbook.md`) |
| API / guardrails | SQL guardrail + agent trace + smoke tests inside `api` container |
| docs only | check Markdown links and terminology |

## Key Files

| Path | Purpose |
|---|---|
| `services/api/app/agent.py` | orchestrator entry point |
| `contracts/semantic_catalog.yaml` | agent-visible Gold surface + allowed joins |
| `dbt/models/schema.yml` | dbt tests and column docs |
| `docs/development-roadmap.md` | phased roadmap + current phase status |
| `docs/modeling-decisions.md` | Gold star schema rationale |
| `docs/runbook.md` | operational procedures |
| `docs/data-contracts.md` | Bronze storage contracts |

## Coding Rules (Claude-specific)

- Prefer editing existing files over creating new ones
- No comments unless the WHY is non-obvious
- No extra abstractions beyond the task scope
- After finishing a roadmap phase, update `docs/development-roadmap.md` with status + next step
- Before any architecture change, read `docs/modeling-decisions.md`
- dbt model changes: update `dbt/models/schema.yml` in the same change
- Ingestion path changes: update `docs/runbook.md` and `docs/data-contracts.md`
