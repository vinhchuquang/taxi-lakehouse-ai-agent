# Tài liệu gửi AI để viết Chương 3 — "Cài đặt hệ thống"

Thư mục này gom các tài liệu kỹ thuật cần thiết để một AI viết Chương 3 của báo
cáo tốt nghiệp (Data Lakehouse + AI Agent Text-to-SQL cho dữ liệu taxi NYC TLC).

## Cách dùng

1. Gửi/upload **toàn bộ** các file trong thư mục này cho AI.
2. Gửi kèm **nội dung Chương 1 và Chương 2** (trích từ file PDF báo cáo) — để AI
   nắm văn phong và mạch thiết kế, viết Chương 3 cho liền mạch.
3. Dán prompt ở mục cuối file này.

## LƯU Ý QUAN TRỌNG

- Các file `.md` ở đây viết theo cấu trúc **6 chương** của tài liệu nội bộ
  (`thesis-outline.md`). **Báo cáo thật chỉ có 3 chương**, Chương 3 là
  "Cài đặt hệ thống". Hãy yêu cầu AI **bỏ qua cách đánh số chương** trong các file
  này, chỉ lấy **dữ kiện kỹ thuật**.
- Không thêm số liệu/benchmark nào ngoài các tài liệu này. Nếu cần minh họa thêm
  phải ghi rõ "ví dụ minh họa".

## Nội dung thư mục

### Nhóm 1 — Bắt buộc (xương sống chương cài đặt)

| File | Phục vụ mục Chương 3 |
|---|---|
| `runbook.md` | 3.1 / 3.2 / 3.3 — lệnh chạy thật (docker compose, dbt build) |
| `architecture.md` | 3.1 — 7 service Docker + luồng dữ liệu |
| `data-contracts.md` | 3.2 — Bronze, atomic download, SHA-256, MinIO |
| `gold-star-schema.md` | 3.3 — 12 model dbt + star schema |
| `semantic_catalog.yaml` | 3.4 / 3.5 — hợp đồng ngữ nghĩa: bảng/cột/JOIN cho phép |
| `agent-evaluation.md` | 3.7 — phương pháp + kết quả đánh giá 27 case |
| `agent-evaluation-results.json` | 3.7 — số liệu thô 27/27, latency p50/p95 |

### Nhóm 2 — Bổ sung chi tiết kết quả/đánh giá

| File | Phục vụ mục Chương 3 |
|---|---|
| `data-quality-report.md` | 3.3 / 3.7 — 77 dbt tests, ~18M dòng bị loại ở Silver |
| `performance-report.md` | 3.7 — phân tích độ trễ |
| `test-results-report.md` | 3.7 — kết quả pytest |
| `architecture-diagrams.md` | 3.1 / 3.5 — sơ đồ kiến trúc + state machine agent |
| `demo-scenarios.md` | 3.6 / 3.7 — kịch bản demo Streamlit |

## Số liệu thật cốt lõi (để đối chiếu nhanh)

- 7 service Docker: `minio, airflow-postgres, airflow-init, airflow-webserver,
  airflow-scheduler, api, demo`. Lệnh chạy: `docker compose up -d`.
- DAG `taxi_monthly_pipeline`: chạy ngày 15 hàng tháng, lookback 3 tháng.
- dbt: 12 model = 3 Bronze + 1 Silver + 6 Gold (1 fact + 5 dim) + 2 mart.
  77 dbt tests pass, 2 anomaly warning. Silver loại ~18M dòng / 116M+ tổng.
- API FastAPI: `/healthz`, `/api/v1/schema`, `/api/v1/query`. Engine: DuckDB.
- Agent phi trạng thái: intent → plan → sinh SQL (OpenAI) → guardrails (sqlglot)
  → thực thi chỉ đọc DuckDB → self-check → phản hồi.
- Guardrails 3 tầng: column / table / join. Chỉ 1 câu SELECT; chặn DML/DDL;
  tự giới hạn LIMIT; tối đa 1 vòng repair.
- Streamlit: tab Schema / SQL / Ask AI / Charts; hiển thị agent_steps; xuất CSV.
- Kiểm thử: pytest 44 pass, 2 skipped.
- Đánh giá agent: 27/27 PASS (100%) = 13 answer + 3 clarification + 11 blocked;
  grounded_answer_rate = 100%; unsafe_rejection_rate = 100%.
- Độ trễ: overall p50 = 92ms, p95 = 2472ms; answer p50 = 753ms, p95 = 2935ms.
- Phạm vi dữ liệu cố định: 2024-01-01 → 2024-06-30 (2024-H1).

---

## Prompt gửi AI

```text
Bạn là trợ lý viết luận văn tốt nghiệp kỹ thuật bằng tiếng Việt học thuật.
Hãy viết HOÀN CHỈNH "Chương 3 — Cài đặt hệ thống" cho đồ án tốt nghiệp của tôi.

# Bối cảnh đề tài
Đồ án xây dựng một Data Lakehouse cục bộ cho dữ liệu chuyến đi taxi NYC TLC
(Yellow + Green Taxi), tổ chức theo các tầng Bronze – Silver – Gold, kèm một
AI Agent Text-to-SQL CHỈ ĐỌC truy vấn trên tầng Gold qua một lớp ngữ nghĩa
có kiểm soát. Toàn bộ chạy local-first bằng Docker. Phạm vi dữ liệu cố định:
2024-01-01 đến 2024-06-30 (2024-H1).

# Tài liệu kèm theo
Tôi đính kèm các file kỹ thuật (runbook, architecture, data-contracts,
gold-star-schema, semantic_catalog.yaml, agent-evaluation, các báo cáo kết quả)
cùng nội dung Chương 1 và Chương 2. Các file kỹ thuật dùng để lấy DỮ KIỆN CHÍNH
XÁC. Hãy BỎ QUA cách đánh số chương trong các file đó; báo cáo của tôi chỉ có 3
chương, Chương 3 là "Cài đặt hệ thống".

# Yêu cầu phân biệt chương (BẮT BUỘC)
Chương 2 đã nói rõ phần thiết kế KHÔNG đi sâu vào lệnh chạy và cấu hình. Vì vậy
Chương 3 phải là chương HIỆN THỰC HÓA: đi vào lệnh chạy cụ thể, cấu hình, cấu
trúc mã nguồn, kết quả build và kết quả kiểm thử thực tế. KHÔNG lặp lại lý do
thiết kế đã có ở Chương 2; chỉ tham chiếu ngắn rồi tập trung "cài đặt thế nào"
và "chạy ra kết quả gì".

# Cấu trúc Chương 3 cần viết (giữ đúng thứ tự, đánh số 3.1–3.8)
3.1 Môi trường và công nghệ triển khai (Docker Compose 7 service, lệnh khởi chạy)
3.2 Cài đặt pipeline thu thập dữ liệu bằng Airflow (DAG, manifest, atomic, SHA-256, MinIO)
3.3 Cài đặt mô hình hóa dữ liệu bằng dbt (12 model 3 tầng, lệnh dbt build, dbt tests)
3.4 Cài đặt lớp ngữ nghĩa và API truy vấn FastAPI (semantic catalog, endpoint, module)
3.5 Cài đặt AI Agent Text-to-SQL và hệ guardrails 3 tầng (state machine, sqlglot, repair)
3.6 Cài đặt giao diện minh họa Streamlit (các tab, hiển thị agent_steps)
3.7 Kết quả cài đặt và kiểm thử (pytest, đánh giá agent 27/27, độ trễ, ảnh demo)
3.8 Kết luận chương

# Số liệu/sự kiện THẬT phải dùng (KHÔNG bịa thêm con số ngoài danh sách này)
- 7 service Docker: minio, airflow-postgres, airflow-init, airflow-webserver,
  airflow-scheduler, api, demo. Lệnh: `docker compose up -d`.
- DAG taxi_monthly_pipeline: chạy ngày 15 hàng tháng, lookback 3 tháng; tải
  atomic qua temp file → SHA-256 → upload MinIO kèm metadata.
- dbt: 12 model = 3 Bronze (bronze_yellow_trips, bronze_green_trips,
  bronze_taxi_zone_lookup) + 1 Silver (silver_trips_unified) + 6 Gold (fact_trips,
  dim_date, dim_zone, dim_service_type, dim_vendor, dim_payment_type) + 2 mart
  (gold_daily_kpis, gold_zone_demand). 77 dbt tests pass, 2 anomaly warning. Silver
  loại ~18 triệu dòng bất thường trên tổng 116 triệu+.
- API FastAPI: /healthz, /api/v1/schema, /api/v1/query. Module: agent.py,
  text_to_sql.py, sql_guardrails.py, query_engine.py, catalog.py, audit.py,
  main.py, models.py, config.py. Engine truy vấn: DuckDB.
- Agent phi trạng thái: intent → plan → sinh SQL (OpenAI) → guardrails (sqlglot)
  → thực thi chỉ đọc DuckDB → self-check → đóng gói phản hồi. Đầu ra gồm: summary,
  answer, sql, columns, rows, execution_ms, agent_steps, warnings, confidence,
  requires_clarification, clarification_question.
- Guardrails 3 tầng: (1) column — chỉ cột trong semantic catalog, chặn wildcard
  trên fact_trips; (2) table — chỉ bảng execution_enabled=true, chặn Bronze/Silver;
  (3) join — chỉ allowed_joins, chặn cartesian/thiếu ON. Chỉ đúng 1 câu SELECT;
  chặn INSERT/UPDATE/DELETE/DROP/CREATE/ALTER; tự thêm/giới hạn LIMIT theo
  max_rows; cho tối đa 1 vòng repair, sửa xong phải kiểm tra lại từ đầu.
- Streamlit demo: tab Schema / SQL / Ask AI / Charts; hiển thị agent_steps; xuất CSV.
- Kiểm thử: pytest 44 pass, 2 skipped.
- Đánh giá agent: 27/27 case PASS (100%) = 13 answer + 3 clarification + 11 blocked;
  grounded_answer_rate = 100%; unsafe_rejection_rate = 100%; trace_complete_rate = 100%.
- Độ trễ: overall p50 = 92ms, p95 = 2472ms; answer p50 = 753ms, p95 = 2935ms.

# Yêu cầu trình bày
- Văn phong học thuật, trang trọng, mạch lạc, ngôi trung tính; KHÔNG dùng "tôi/chúng tôi".
- Viết thành đoạn văn liền mạch là chính; chỉ dùng gạch đầu dòng cho danh sách
  lệnh/endpoint/bước xử lý.
- Mỗi mục mở đầu bằng 1–2 câu nối với thiết kế ở Chương 2, rồi đi vào cài đặt.
- Chèn các khối lệnh tiêu biểu (docker compose, dbt build, gọi /api/v1/query…)
  dưới dạng code block ngắn, kèm giải thích.
- Đề xuất vị trí HÌNH (ảnh Airflow DAG, giao diện Streamlit, một agent trace mẫu)
  và BẢNG (bảng tổng hợp 27 case theo 3 nhóm, bảng độ trễ) bằng chú thích
  "Hình 3.x: ..." / "Bảng 3.x: ..." để tôi tự chèn ảnh sau.
- Độ dài khoảng 6–9 trang A4.
- Kết thúc bằng mục 3.8 tóm tắt phần đã hiện thực hóa và nối sang Kết luận.

# Ràng buộc
- Không thêm tính năng ngoài phạm vi (FHV/HVFHV, streaming, agent ghi dữ liệu).
- Không thêm số liệu/benchmark ngoài danh sách trên; cần minh họa thêm phải ghi
  rõ "ví dụ minh họa".
- Giữ nhất quán thuật ngữ với Chương 1 và 2 (Bronze/Silver/Gold, star schema,
  semantic catalog, guardrails, Text-to-SQL, ELT).
```
