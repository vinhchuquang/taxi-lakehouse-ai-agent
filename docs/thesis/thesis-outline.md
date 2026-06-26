# Đề cương Báo cáo Tốt nghiệp

Tài liệu này map 41 phases trong [development-roadmap.md](../development-roadmap.md)
vào 6 chương báo cáo tốt nghiệp chuẩn. Mục đích: cung cấp khung viết để chuyển từ
"code đã xong" sang "báo cáo có thể bảo vệ".

- Dataset cố định: `2024-01-01` đến `2024-06-30` (2024-H1).
- Kết quả đánh giá tham chiếu: [agent-evaluation-results.json](../agent-evaluation-results.json) — 27/27 PASS.
- Phạm vi cố định: Yellow + Green Taxi, đọc-only agent, local-first.

---

## Chương 1. Giới thiệu (Introduction)

### 1.1 Bối cảnh và động lực
- NYC TLC công bố dữ liệu chuyến đi taxi công khai theo tháng, khối lượng hàng
  trăm triệu chuyến/năm — bài toán điển hình cho data lakehouse.
- Xu hướng lakehouse (Bronze/Silver/Gold) kết hợp lưu trữ object storage chi phí
  thấp với khả năng truy vấn SQL như data warehouse.
- AI agent đọc-only trên Gold cho phép phân tích dữ liệu bằng ngôn ngữ tự nhiên
  trong khi vẫn đảm bảo an toàn (không DML/DDL, không lộ dữ liệu thô).

### 1.2 Mục tiêu đồ án
1. Xây dựng pipeline ingestion → Bronze → Silver → Gold lặp lại được (repeatable).
2. Mô hình hóa Gold theo Kimball star schema + aggregate marts phục vụ analytics.
3. Triển khai AI query agent đọc-only với guardrails nhiều tầng.
4. Đánh giá định lượng độ chính xác, độ an toàn và độ trễ của agent.

### 1.3 Phạm vi và giới hạn
- **Trong phạm vi**: Yellow Taxi, Green Taxi, Taxi Zone Lookup; cửa sổ `2024-H1`;
  local-first (Docker); read-only agent.
- **Ngoài phạm vi** (đã được khoanh vùng rõ trong [AGENTS.md](../../AGENTS.md)):
  FHV/HVFHV, streaming, write-capable agent, multi-tenant auth, cloud production.

### 1.4 Đóng góp chính
1. Một lakehouse MVP hoàn chỉnh chạy local hoàn toàn bằng Docker.
2. Star schema Kimball có kiểm chứng (dbt tests, anomaly classification).
3. Read-only agent orchestrator tự xây — không phụ thuộc LangChain/Vanna —
   với 3 tầng guardrails (column/wildcard/join).
4. Bộ đánh giá hồi quy 27 cases (13 answer + 3 clarification + 11 blocked)
   với 100% pass rate, được lưu vết JSONL cho khả năng tái lập.

### 1.5 Cấu trúc báo cáo
*Tóm tắt 5 chương còn lại trong 1 đoạn.*

---

## Chương 2. Cơ sở lý thuyết và các nghiên cứu liên quan

→ Nguồn chi tiết: [related-work.md](related-work.md).

### 2.1 Kiến trúc Lakehouse
- Mô hình medallion (Bronze → Silver → Gold) của Databricks.
- So sánh Lakehouse với Data Warehouse truyền thống và Data Lake.

### 2.2 Dimensional Modeling (Kimball)
- Star schema, fact và dimension table, conformed dimensions.
- Lý do chọn star schema cho Gold layer của đồ án (xem
  [modeling-decisions.md](../modeling-decisions.md)).

### 2.3 Modern Data Stack
- Vai trò của Airflow (orchestration), dbt (transformation), DuckDB (analytical
  engine), MinIO (object storage).

### 2.4 Text-to-SQL và AI Agents
- Tổng quan các hệ Text-to-SQL (Spider benchmark, RAT-SQL, T5-based).
- Khái niệm "agent workflow": intent → planning → tool calling → self-check.
- Vấn đề an toàn của Text-to-SQL: SQL injection, hallucination, schema misuse.

### 2.5 SQL Guardrails
- Validation tĩnh bằng AST parsing (sqlglot).
- So sánh allow-list vs deny-list approach.

### 2.6 Khoảng trống mà đồ án giải quyết
- Đa số sample Text-to-SQL không có guardrails đủ mạnh để chạy production.
- Đa số khung agent (LangChain, Vanna) giấu workflow → khó debug và đánh giá.
- Đồ án xây custom agent để có khả năng trace toàn bộ workflow.

---

## Chương 3. Thiết kế hệ thống

### 3.1 Kiến trúc tổng thể
- Sơ đồ thành phần: 7 services Docker.
- Sơ đồ luồng dữ liệu Bronze → Silver → Gold.
- → Nguồn: [architecture.md](../architecture.md), [architecture-diagrams.md](architecture-diagrams.md).
- **Phase liên quan**: 1, 7A.

### 3.2 Lớp Bronze và Data Contracts
- MinIO làm Bronze source of truth.
- Atomic download + SHA-256 checksum + classification (verified/unverified).
- → Nguồn: [data-contracts.md](../data-contracts.md).
- **Phase liên quan**: 1, 5B, 25.

### 3.3 Lớp Silver — Chuẩn hóa schema
- Unified schema giữa Yellow và Green.
- Validity filters: pickup date trong tháng partition, dropoff sau pickup,
  amount > 0, distance hợp lệ.
- **Phase liên quan**: 1, 2.

### 3.4 Lớp Gold — Star Schema
- 1 fact + 5 dimensions: `fact_trips`, `dim_date`, `dim_zone`, `dim_service_type`,
  `dim_vendor`, `dim_payment_type`.
- 2 aggregate marts: `gold_daily_kpis`, `gold_zone_demand`.
- → Nguồn: [gold-star-schema.md](../gold-star-schema.md), [modeling-decisions.md](../modeling-decisions.md).
- **Phase liên quan**: 3, 4.

### 3.5 Semantic Catalog
- File [contracts/semantic_catalog.yaml](../../contracts/semantic_catalog.yaml) làm
  hợp đồng giữa Gold và agent: cho phép bảng/cột/JOIN nào.
- **Phase liên quan**: 6, 11A.

### 3.6 AI Agent Orchestrator
- State machine: Intent classify → Plan → Generate/Override SQL → Guardrails
  validate → Execute → Self-check → Answer.
- Deterministic answer là mặc định; OpenAI synthesis là tùy chọn.
- → Nguồn: [services/api/app/agent.py](../../services/api/app/agent.py),
  [architecture-diagrams.md](architecture-diagrams.md).
- **Phase liên quan**: 9, 11B–11G, 27.

### 3.7 Hệ Guardrails 3 tầng
- **Column guardrails**: chỉ cột trong semantic catalog, chặn wildcard trên
  `fact_trips`.
- **Table guardrails**: chỉ bảng `execution_enabled = true`.
- **Join guardrails**: chỉ JOIN theo `allowed_joins`, chặn cartesian/missing ON.
- **Phase liên quan**: 7B, 8.

---

## Chương 4. Triển khai (Implementation)

### 4.1 Môi trường và stack triển khai
- Docker Compose: minio, postgres, airflow-init, airflow-scheduler,
  airflow-webserver, api, demo.
- Cài đặt: `docker compose up -d`.
- → Nguồn: [runbook.md](../runbook.md).

### 4.2 Ingestion Pipeline (Airflow)
- DAG `taxi_monthly_pipeline` — lịch chạy ngày 15 hàng tháng, lookback 3 tháng.
- Atomic download qua temp file → SHA-256 → upload MinIO với metadata.
- Pipeline run metadata được lưu durable tại
  `metadata/pipeline_runs/taxi_monthly_pipeline/...`.
- **Phase liên quan**: 10B, 25, 26.

### 4.3 dbt Transformation
- 12 models: 3 Bronze + 1 Silver + 6 Gold (5 dim + 1 fact) + 2 marts.
- 77 dbt tests (pass) + 2 anomaly warnings (documented).
- → Nguồn: [dbt/models/](../../dbt/models/), [data-quality-report.md](../data-quality-report.md).
- **Phase liên quan**: 2, 3, 4, 13.

### 4.4 FastAPI Service
- Endpoints: `/api/v1/schema`, `/api/v1/query`, `/healthz`.
- Module chính: `agent.py`, `text_to_sql.py`, `sql_guardrails.py`,
  `query_engine.py`, `catalog.py`, `audit.py`.
- → Nguồn: [services/api/app/](../../services/api/app/).

### 4.5 Streamlit Demo UI
- 4 tab: Schema, SQL, Ask AI, Charts.
- Hiển thị `agent_steps` để demo workflow.
- → Nguồn: [services/demo/](../../services/demo/).
- **Phase liên quan**: 10C, 11G, 15.

### 4.6 Tooling và DevOps
- `python -m pytest -p no:cacheprovider` — 44 pass, 2 skipped.
- CI/CD và release packaging.
- **Phase liên quan**: 18, 36.

---

## Chương 5. Đánh giá (Evaluation)

→ Nguồn phương pháp: [evaluation-methodology.md](evaluation-methodology.md).

### 5.1 Phương pháp đánh giá
- 3 trục: Data quality, Agent correctness/safety, Performance.
- Reproducibility: defense dataset đóng băng tại `2024-H1`.

### 5.2 Data Quality
- dbt tests: 77 pass / 2 warn / 0 error.
- Silver loại ~18M anomaly rows từ tổng 116M+.
- → Nguồn: [data-quality-report.md](../data-quality-report.md).
- **Phase liên quan**: 13.

### 5.3 Agent Correctness và Safety
- **Total**: 27/27 PASS (100%).
- **Answer cases**: 13/13 — mart + star schema queries.
- **Clarification cases**: 3/3 — câu hỏi mơ hồ được hỏi lại an toàn.
- **Blocked cases**: 11/11 — DDL/DML, Silver access, wildcard, invalid joins.
- **Grounded answer rate**: 100%.
- → Nguồn: [agent-evaluation-results.json](../agent-evaluation-results.json).
- **Phase liên quan**: 14, 28, 37.

### 5.4 Performance
- Latency overall p50 = 92ms, p95 = 2472ms.
- Answer cases p50 = 753ms, p95 = 2935ms.
- Benchmark 5 query đại diện — quyết định giữ Gold ở dạng view (đủ nhanh).
- → Nguồn: [performance-report.md](../performance-report.md),
  [performance-benchmark-results.json](../performance-benchmark-results.json).
- **Phase liên quan**: 17.

### 5.5 Hạn chế và threats to validity
- Test set 27 case do tác giả tự thiết kế — có khả năng selection bias.
- Không có ground truth do bên ngoài label.
- Đánh giá đơn lượt (single-turn), chưa đánh giá multi-turn.
- Cửa sổ dữ liệu hẹp (6 tháng) so với toàn bộ TLC.

---

## Chương 6. Kết luận và Hướng phát triển

### 6.1 Kết quả đạt được
- Lakehouse local-first chạy được end-to-end, tái lập trong vài lệnh.
- Agent đọc-only an toàn 100% trên test set, có khả năng trace toàn bộ workflow.
- Đánh giá có bằng chứng định lượng, dataset cố định.

### 6.2 Hạn chế của đồ án
- Local-first, chưa thử nghiệm trên dữ liệu sản xuất.
- Single-turn agent, chưa hỗ trợ hội thoại nhiều lượt.
- Không cover FHV/HVFHV.

### 6.3 Hướng phát triển
→ Nguồn chi tiết: [production-roadmap.md](production-roadmap.md).
- Mở rộng nguồn (FHV/HVFHV) với contracts mới.
- Thêm streaming ingestion (Kafka/Debezium).
- Multi-turn agent + caching.
- Production deployment: Kubernetes, monitoring, alerting.

---

## Phụ lục đề xuất

- **Phụ lục A** — Demo scenarios (12 cases): [demo-scenarios.md](../demo-scenarios.md)
- **Phụ lục B** — Runbook: [runbook.md](../runbook.md)
- **Phụ lục C** — Sample agent traces: [agent-evaluation-results.json](../agent-evaluation-results.json)
- **Phụ lục D** — Release checklist: [release-checklist.md](../release-checklist.md)
- **Phụ lục E** — Security notes: [security-notes.md](../security-notes.md)

---

## Map nhanh: Phase → Chương

| Phase | Chương báo cáo |
|---|---|
| 1, 2 | Ch.3.2–3.3, Ch.4.2 |
| 3, 4 | Ch.3.4 |
| 5, 5B | Ch.3.2 |
| 6 | Ch.3.5 |
| 7A | Ch.3.1 |
| 7B, 8 | Ch.3.7 |
| 9, 11A–11G, 27 | Ch.3.6 |
| 10, 10B, 10C | Ch.4.2, Ch.4.5 |
| 12 | Ch.5.1 |
| 13 | Ch.5.2 |
| 14, 28, 37 | Ch.5.3 |
| 15, 32 | Ch.4.5 |
| 16, 19, 25, 26 | Ch.4.2, Ch.4.6 |
| 17 | Ch.5.4 |
| 18, 36 | Ch.4.6 |
| 20, 21, 33, 34 | Ch.1, Ch.6 |
| 22, 29, 38 | Ch.5.1 (rehearsal) |
| 23, 24, 30, 31, 35 | (operational, không vào báo cáo chính) |
| 39, 40, 41 | Ch.6.3 (post-defense) |
