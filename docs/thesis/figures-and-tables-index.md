# Danh mục Hình và Bảng

Danh mục hệ thống các **hình vẽ**, **bảng**, và **đoạn mã** cần đưa vào báo
cáo tốt nghiệp. Mỗi mục có: chương đề xuất, nguồn dữ liệu, ghi chú cách
chuẩn bị.

> Quy ước:
> - Hình: `Hình X.Y` — X là chương, Y là thứ tự trong chương.
> - Bảng: `Bảng X.Y` — tương tự.
> - Listing/Code: `Đoạn mã X.Y` (hoặc "Mã nguồn X.Y").
> - Đảm bảo mỗi hình/bảng được **tham chiếu trong thân bài ít nhất một
>   lần** trước khi xuất hiện.

---

## A. Danh mục Hình vẽ

| Mã | Tên hình | Chương | Nguồn | Ghi chú chuẩn bị |
|---|---|---|---|---|
| Hình 2.1 | Mô hình Lakehouse 3 lớp Bronze/Silver/Gold | 2.1 | [related-work #1] | Vẽ minh họa đơn giản (3 hộp xếp dọc + mũi tên) |
| Hình 2.2 | Star schema mẫu Kimball | 2.2 | [related-work #4] | Vẽ minh họa 1 fact + 4 dim |
| Hình 2.3 | Vị trí Text-to-SQL trong pipeline AI agent | 2.4 | Tự vẽ | Sơ đồ: user → NL → planner → SQL → executor → answer |
| Hình 3.1 | Kiến trúc thành phần hệ thống (7 service Docker) | 3.1 | [architecture-diagrams.md](architecture-diagrams.md) Figure 1 | Render Mermaid Figure 1 → PNG/SVG |
| Hình 3.2 | Luồng dữ liệu Bronze → Silver → Gold | 3.2 | [architecture-diagrams.md](architecture-diagrams.md) Figure 2 | Render Mermaid Figure 2 |
| Hình 3.3 | Sơ đồ star schema lớp Gold của đồ án | 3.4 | [gold-star-schema.md](../gold-star-schema.md) | Vẽ riêng: `fact_trips` ở giữa + 5 dim xung quanh |
| Hình 3.4 | Máy trạng thái AI agent (7 trạng thái) | 3.6 | [architecture-diagrams.md](architecture-diagrams.md) Figure 3 | Render Mermaid Figure 3 |
| Hình 3.5 | Pipeline guardrails 3 tầng | 3.7 | [architecture-diagrams.md](architecture-diagrams.md) Figure 4 | Render Mermaid Figure 4 |
| Hình 3.6 | Vòng đời pipeline run metadata | 3.2 / 4.2 | [architecture-diagrams.md](architecture-diagrams.md) Figure 5 | Render Mermaid Figure 5 (sequence) |
| Hình 4.1 | Sơ đồ DAG `taxi_monthly_pipeline` trên Airflow UI | 4.2 | Screenshot Airflow | Mở `http://localhost:8080` → DAG graph view |
| Hình 4.2 | Streamlit demo — tab Schema | 4.5 | Screenshot | Bật stack, mở `http://localhost:8501` |
| Hình 4.3 | Streamlit demo — tab Ask AI với `agent_steps` | 4.5 | Screenshot | Chạy 1 câu hỏi answer, mở rộng trace |
| Hình 4.4 | Streamlit demo — tab Charts | 4.5 | Screenshot | Chạy 1 query có biểu đồ |
| Hình 5.1 | Phân bố latency 27 cases | 5.4 | [agent-evaluation-results.json](../agent-evaluation-results.json) | Box plot hoặc histogram theo `elapsed_ms` |
| Hình 5.2 | So sánh latency: aggregate_mart vs star_schema | 5.4 | [agent-evaluation-results.json](../agent-evaluation-results.json) | Bar chart p50/p95 hai surface |
| Hình 6.1 | Roadmap phát triển sau bảo vệ (7 phases F1–F7) | 6.3 | [production-roadmap.md](production-roadmap.md) §10 | Gantt-style hoặc bảng có effort/risk |

**Số lượng đề xuất:** 14–16 hình. Hội đồng đánh giá tốt khi có hình rõ ràng
trong các phần thiết kế (Chương 3) và đánh giá (Chương 5).

---

## B. Danh mục Bảng

| Mã | Tên bảng | Chương | Nguồn | Ghi chú |
|---|---|---|---|---|
| Bảng 1.1 | Tóm tắt phạm vi (in scope / out of scope) | 1.3 | [AGENTS.md](../../AGENTS.md) | 2 cột, ~6 dòng mỗi cột |
| Bảng 2.1 | So sánh Data Lake / Data Warehouse / Lakehouse | 2.1 | [related-work #1] | 3 cột × 4–5 thuộc tính |
| Bảng 2.2 | Stack công cụ và vai trò | 2.3 | [related-work #6–#10] | 5 dòng × 3 cột (công cụ, vai trò, lý do chọn) |
| Bảng 3.1 | Mô tả 7 service Docker | 3.1 | [docker-compose.yml](../../docker-compose.yml) | Cột: service, role, port, dependency |
| Bảng 3.2 | Các model dbt theo lớp | 3.4 / 4.3 | [dbt/models/](../../dbt/models/) | 12 models, cột: layer/name/grain |
| Bảng 3.3 | Các tầng guardrail và quy tắc | 3.7 | [services/api/app/sql_guardrails.py](../../services/api/app/sql_guardrails.py) | 3 tầng × ~3 quy tắc |
| Bảng 4.1 | Endpoint của FastAPI service | 4.4 | [services/api/app/main.py](../../services/api/app/main.py) | 3 dòng: method, path, mục đích |
| Bảng 5.1 | dbt test summary | 5.2 | [data-quality-report.md](../data-quality-report.md) | Pass/Warn/Error/Skip × layer |
| Bảng 5.2 | Chi tiết 11 blocked cases × trục guardrail | 5.3 | [agent-evaluation-results.json](../agent-evaluation-results.json) | Cột: case_id, trục, kỳ vọng, kết quả |
| Bảng 5.3 | Bảng metric đánh giá agent | 5.3 | [evaluation-methodology.md](evaluation-methodology.md) §3 | 6 dòng metric × giá trị |
| Bảng 5.4 | Latency theo surface | 5.4 | [agent-evaluation-results.json](../agent-evaluation-results.json) §latency_ms | aggregate_mart vs star_schema, p50/p95 |
| Bảng 5.5 | 5 truy vấn benchmark Phase 17 | 5.4 | [performance-report.md](../performance-report.md) | Cột: query, median, rows |
| Bảng 5.6 | Hạn chế và threats to validity | 5.5 | [evaluation-methodology.md](evaluation-methodology.md) §7 | 5–7 dòng |
| Bảng 6.1 | Phasing hướng phát triển F1–F7 | 6.3 | [production-roadmap.md](production-roadmap.md) §10 | Cột: phase, theme, effort, risk |

**Số lượng đề xuất:** 13–15 bảng.

---

## C. Danh mục Đoạn mã (Code Listings)

Đoạn mã chỉ trích những phần **có giá trị giải thích thiết kế**. Tránh chèn
nguyên file dài — chọn 10–20 dòng đại diện.

| Mã | Tên đoạn mã | Chương | Nguồn | Cách trích |
|---|---|---|---|---|
| Đoạn mã 3.1 | Một entry trong `semantic_catalog.yaml` | 3.5 | [contracts/semantic_catalog.yaml](../../contracts/semantic_catalog.yaml) | Trích 1 entry cho `fact_trips` với `execution_enabled`, `columns`, `allowed_joins` (~15 dòng) |
| Đoạn mã 3.2 | Hàm guardrail kiểm tra wildcard | 3.7 | [services/api/app/sql_guardrails.py](../../services/api/app/sql_guardrails.py) | Function chính, ~10–15 dòng |
| Đoạn mã 3.3 | State machine của agent | 3.6 | [services/api/app/agent.py](../../services/api/app/agent.py) | Đoạn `def run(...)` thể hiện 7 bước, ~20 dòng |
| Đoạn mã 4.1 | DAG `taxi_monthly_pipeline` (khung) | 4.2 | [airflow/dags/taxi_monthly_pipeline.py](../../airflow/dags/taxi_monthly_pipeline.py) | Bỏ phần boilerplate, giữ task definition |
| Đoạn mã 4.2 | Model dbt `silver_trips_unified` (rút gọn) | 4.3 | [dbt/models/silver/silver_trips_unified.sql](../../dbt/models/silver/) | Giữ phần UNION + validity filters |
| Đoạn mã 4.3 | Response JSON của `/api/v1/query` (đã rút gọn) | 4.4 | API thực tế | Chạy 1 query, copy response, rút gọn rows |
| Đoạn mã 5.1 | Snippet từ `agent-evaluation-results.json` | 5.3 | [agent-evaluation-results.json](../agent-evaluation-results.json) | Lấy 1 case answer + 1 case blocked |

**Số lượng đề xuất:** 6–8 đoạn mã. Quy tắc: nếu một slide hay paragraph cần
giải thích "code làm gì", chèn đoạn mã. Nếu không, mô tả bằng văn xuôi và
trỏ về file trong repo.

---

## D. Phụ lục đề xuất (đi với mục lục cuối báo cáo)

| Phụ lục | Nội dung | Nguồn |
|---|---|---|
| Phụ lục A | 12 demo scenarios cho buổi bảo vệ | [demo-scenarios.md](../demo-scenarios.md) |
| Phụ lục B | Runbook khởi động hệ thống | [runbook.md](../runbook.md) |
| Phụ lục C | Snapshot `agent-evaluation-results.json` đầy đủ | [agent-evaluation-results.json](../agent-evaluation-results.json) |
| Phụ lục D | Snapshot `performance-benchmark-results.json` | [performance-benchmark-results.json](../performance-benchmark-results.json) |
| Phụ lục E | Release checklist Phase 18 | [release-checklist.md](../release-checklist.md) |
| Phụ lục F | Security notes | [security-notes.md](../security-notes.md) |
| Phụ lục G | Bảng thuật ngữ Việt-Anh | [glossary.md](glossary.md) |

---

## E. Quy ước trình bày

### Hình vẽ
- Đánh số liên tục theo chương: 2.1, 2.2, 3.1, 3.2...
- Caption đặt **dưới** hình.
- Nguồn ngoài (paper, doc khác) phải ghi trong caption: *"Nguồn: [related-work #1]"*.
- File hình lưu vào `docs/figures/` (tạo thư mục mới) với tên có quy ước:
  `fig-3-1-architecture.svg`, `fig-5-2-latency-by-surface.png`...
- Định dạng ưu tiên: SVG cho diagram, PNG cho screenshot.

### Bảng
- Đánh số liên tục theo chương.
- Caption đặt **trên** bảng.
- Bảng dài chia trang phải có header lặp lại.
- Số liệu phải khớp với snapshot mới nhất; nếu không đảm bảo, ghi rõ ngày
  snapshot.

### Đoạn mã
- Dùng font monospace (Consolas, Courier New, …).
- Đánh số dòng nếu trích >10 dòng.
- Ghi rõ đường dẫn file ở caption: *"Đoạn mã 3.1 — Trích từ
  `contracts/semantic_catalog.yaml`"*.
- Đừng paste toàn file — chỉ trích phần có giá trị.

---

## F. Workflow chuẩn bị hình ảnh

1. **Diagram (Hình 3.1–3.5)**:
   - Mở [architecture-diagrams.md](architecture-diagrams.md) → copy block
     Mermaid → paste vào https://mermaid.live → export SVG.
   - Lưu vào `docs/figures/` với tên rõ ràng.

2. **Screenshot (Hình 4.1–4.4)**:
   - `docker compose up -d` để khởi động stack.
   - Mở Airflow / Streamlit, chụp ảnh ở độ phân giải cao.
   - Trim các phần không cần, làm mờ nếu có thông tin nhạy cảm.

3. **Chart (Hình 5.1–5.2)**:
   - Mở [agent-evaluation-results.json](../agent-evaluation-results.json) trong
     Python/Excel.
   - Vẽ box plot hoặc bar chart, export PNG.

4. **Star schema (Hình 3.3)**:
   - Có thể vẽ bằng dbdiagram.io, draw.io, hoặc Mermaid `erDiagram`.
   - Lấy thông tin cột từ [gold-star-schema.md](../gold-star-schema.md).

---

## G. Checklist trước khi nộp báo cáo

- [ ] Mọi hình/bảng đều **được tham chiếu trong thân bài**.
- [ ] Số liệu mọi bảng khớp với snapshot JSON mới nhất.
- [ ] Hình ảnh không bị bể, font legible khi in.
- [ ] Đánh số chương/hình/bảng liên tục, không nhảy số.
- [ ] Caption đầy đủ với nguồn (nếu lấy ngoài).
- [ ] Phụ lục được liệt kê đầy đủ trong mục lục.
- [ ] Mỗi đoạn mã có chú thích đường dẫn file.
