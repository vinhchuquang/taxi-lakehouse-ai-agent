# Architecture Diagrams

Visual companion to [architecture.md](../architecture.md). All diagrams use
[Mermaid](https://mermaid.js.org/) and render natively on GitHub. Use these as
figures in the thesis report.

- Defense window: `2024-01-01` through `2024-06-30`.
- Stack: Docker Compose with MinIO, Airflow, dbt, DuckDB, FastAPI, Streamlit.

---

## Figure 1. System Component Diagram

Logical view of the seven Docker services and their dependencies.

```mermaid
flowchart TB
    subgraph Storage
        MINIO[(MinIO<br/>Bronze + metadata)]
        DUCKDB[(DuckDB<br/>warehouse/analytics.duckdb)]
        PG[(Postgres<br/>Airflow metastore)]
    end

    subgraph Orchestration
        AF_INIT[airflow-init]
        AF_SCHED[airflow-scheduler<br/>DAG: taxi_monthly_pipeline]
        AF_WEB[airflow-webserver<br/>:8080]
    end

    subgraph Serving
        API[FastAPI<br/>:8000<br/>read-only agent]
        DEMO[Streamlit<br/>:8501<br/>demo UI]
    end

    AF_INIT --> PG
    AF_SCHED --> PG
    AF_WEB --> PG
    AF_SCHED -- ingest --> MINIO
    AF_SCHED -- dbt build --> DUCKDB
    AF_SCHED -- pipeline_runs JSON --> MINIO

    API -- read-only --> DUCKDB
    API -- semantic catalog --> CATALOG[/contracts/<br/>semantic_catalog.yaml/]
    DEMO -- HTTP --> API

    USER([User / Defense panel]) --> DEMO
    USER -.cURL.-> API
```

---

## Figure 2. Bronze → Silver → Gold Data Flow

Layered transformation from raw TLC files to the agent-visible Gold surface.

```mermaid
flowchart LR
    TLC[(NYC TLC<br/>Open Data<br/>Yellow + Green + Zones)]

    subgraph Ingestion["Ingestion (Airflow)"]
        DL[Download via temp<br/>SHA-256 verify<br/>atomic promote]
        UP[Upload to MinIO<br/>with metadata]
    end

    subgraph Bronze
        B_Y[bronze_yellow_trips]
        B_G[bronze_green_trips]
        B_Z[bronze_taxi_zone_lookup]
    end

    subgraph Silver
        S[silver_trips_unified<br/>~98M valid rows<br/>~18M anomalies filtered]
    end

    subgraph Gold["Gold (star schema + marts)"]
        F[fact_trips]
        D1[dim_date]
        D2[dim_zone]
        D3[dim_service_type]
        D4[dim_vendor]
        D5[dim_payment_type]
        M1[gold_daily_kpis<br/>fast path]
        M2[gold_zone_demand<br/>fast path]
    end

    TLC --> DL --> UP --> B_Y & B_G & B_Z
    B_Y & B_G --> S
    B_Z --> D2
    S --> F
    F --> M1
    F --> M2
```

**Notes:**
- Bronze stores raw files with minimal mutation.
- Silver applies validity filters: pickup date inside partition month,
  dropoff > pickup, amount > 0, distance plausible.
- Gold is the only surface exposed to the agent.

---

## Figure 3. Read-Only Agent State Machine

Workflow of `services/api/app/agent.py` from user question to answer.

```mermaid
stateDiagram-v2
    [*] --> IntentAnalysis: question + filters
    IntentAnalysis --> Plan: classified intent
    IntentAnalysis --> Clarify: ambiguous
    Plan --> SQLGenerate: deterministic plan
    Plan --> SQLGenerate_LLM: complex plan
    SQLGenerate --> Guardrails
    SQLGenerate_LLM --> Guardrails
    Guardrails --> Execute: PASS
    Guardrails --> Blocked: FAIL
    Execute --> SelfCheck: rows
    SelfCheck --> Answer: grounded
    SelfCheck --> Clarify: result empty / off-target
    Clarify --> [*]
    Blocked --> [*]
    Answer --> [*]
```

**Key properties:**
- Guardrails are mandatory; no execution without PASS.
- Deterministic answer is default; OpenAI synthesis is opt-in and must be
  grounded in executed rows only.
- `agent_steps` are returned in every response for traceability.

---

## Figure 4. SQL Guardrails Pipeline

Layered validation of every generated SQL before execution.

```mermaid
flowchart TD
    SQL_IN[Generated SQL]
    SQL_IN --> P1{Statement type?}
    P1 -- "non-SELECT (DDL/DML)" --> X1[BLOCK]
    P1 -- SELECT --> P2{Tables cataloged?}
    P2 -- no --> X2[BLOCK: unknown table]
    P2 -- yes --> P3{execution_enabled = true?}
    P3 -- no --> X3[BLOCK: disabled table]
    P3 -- yes --> P4{Columns known?<br/>Wildcard on fact_trips?}
    P4 -- bad --> X4[BLOCK: unknown column<br/>or wildcard restricted]
    P4 -- ok --> P5{JOIN has ON?<br/>Path in allowed_joins?}
    P5 -- cartesian / unknown --> X5[BLOCK: invalid join]
    P5 -- ok --> EXEC[Execute on DuckDB read-only<br/>with max_rows]
```

Verified against 11 unsafe cases in
[agent-evaluation-results.json](../agent-evaluation-results.json) — all blocked
(unsafe_rejection_rate = 1.0).

---

## Figure 5. Pipeline Run Metadata Lifecycle

Phase 25 durable observability for every Airflow DAG run.

```mermaid
sequenceDiagram
    participant AF as Airflow Scheduler
    participant ING as Ingestion Task
    participant MINIO as MinIO
    participant DBT as dbt Build Task
    participant META as Pipeline Run Metadata

    AF->>ING: trigger (year, month)
    ING->>MINIO: download + verify + upload
    ING->>META: ingestion status (verified/unverified)
    AF->>DBT: run dbt build
    DBT->>META: pass/warn/error/skip counts
    AF->>META: finalize run_summary.json
    META->>MINIO: persist metadata/pipeline_runs/...
    Note over META: Latest verified run<br/>phase25_2024_01_20260506<br/>quality_gate = passed_with_warnings<br/>dbt = 77/2/0/0
```

---

## Figure 6. Semantic Catalog as Contract

`contracts/semantic_catalog.yaml` is the single source of truth for what the
agent can see.

```mermaid
flowchart LR
    YAML[semantic_catalog.yaml]
    YAML --> SCHEMA[/api/v1/schema endpoint]
    YAML --> COL_G[Column guardrails]
    YAML --> JOIN_G[Join guardrails]
    YAML --> EXEC_G[execution_enabled gate]
    YAML --> PLANNER[Deterministic planner]
    YAML --> PROMPT[LLM SQL prompt context]

    COL_G --> CHECK[/SQL guardrails/]
    JOIN_G --> CHECK
    EXEC_G --> CHECK
    PLANNER --> CHECK
    CHECK --> DUCK[(DuckDB execute)]
```

The catalog covers 8 execution-enabled Gold objects:
- 2 aggregate marts: `gold_daily_kpis`, `gold_zone_demand`
- 1 fact: `fact_trips`
- 5 dimensions: `dim_date`, `dim_zone`, `dim_service_type`, `dim_vendor`,
  `dim_payment_type`

---

## Figure 7. Deployment Topology (Docker)

```mermaid
flowchart TB
    HOST[Host: Docker Compose]

    subgraph Network["compose network"]
        S1[minio :9000/:9001]
        S2[airflow-postgres :5432]
        S3[airflow-init]
        S4[airflow-scheduler]
        S5[airflow-webserver :8080]
        S6[api :8000]
        S7[demo :8501]
    end

    HOST --> Network
    USER([Localhost browser]) -.-> S5
    USER -.-> S7
    USER -.-> S6
    USER -.-> S1

    S3 --> S2
    S4 --> S2
    S5 --> S2
    S4 -.s3 protocol.-> S1
    S6 -.read-only DuckDB.-> VOL[(warehouse volume)]
    S4 -.write.-> VOL
```

---

## How to render in the thesis report

1. **For Word/Google Docs**: use [mermaid.live](https://mermaid.live) — paste
   each block, export PNG/SVG, embed as figure.
2. **For LaTeX**: convert SVG via `mermaid-cli` (`mmdc -i diagram.mmd -o
   diagram.pdf`).
3. **For PDF preview in IDE**: install the Markdown Preview Mermaid Support
   extension (VS Code).

Each figure should appear in the report with caption (`Hình 3.1`, `Hình 3.2`...)
matching the section in [thesis-outline.md](thesis-outline.md) Ch.3.
