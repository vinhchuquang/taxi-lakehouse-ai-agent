# Chương 4 — Cài đặt & kiểm thử

**Mục tiêu chương:** hiện thực hóa + kịch bản kiểm thử + đo đầy đủ thông số +
**benchmark agent** (Spider so leaderboard + bộ test riêng).

**Tái dùng từ báo cáo cũ:** Chương 3 cũ (cài đặt) — **đã có bản sửa lỗi**. Mở rộng mạnh đánh giá.

## Tài liệu cần đính kèm khi gửi AI
- **Chương 3 báo cáo cũ** (`main (14).pdf`) ✅ + [chuong3-sua-loi.md](chuong3-sua-loi.md) ✅ (áp dụng sửa lỗi)
- [../runbook.md](../runbook.md) ✅
- [../data-quality-report.md](../data-quality-report.md), [../performance-report.md](../performance-report.md) ✅
- [../agent-evaluation.md](../agent-evaluation.md), [../agent-evaluation-results.json](../agent-evaluation-results.json) ✅
- [../thesis/evaluation-methodology.md](../thesis/evaluation-methodology.md) ✅
- [../demo-scenarios.md](../demo-scenarios.md) ✅
- **Kết quả benchmark Spider** ❌ *(chưa có — phải chạy trước khi viết 4.10.2; xem [cai-thien-do-an.md](cai-thien-do-an.md) mục B1)*

---

## PROMPT (copy nguyên khối dưới đây)

```text
Bạn là trợ lý viết luận văn tốt nghiệp kỹ thuật bằng tiếng Việt học thuật.

# Bối cảnh đề tài
Đồ án xây dựng một Data Lakehouse cục bộ cho dữ liệu chuyến đi taxi NYC TLC
(Yellow + Green Taxi), tổ chức theo các tầng Bronze – Silver – Gold, kèm một
AI Agent Text-to-SQL CHỈ ĐỌC truy vấn trên tầng Gold qua một lớp ngữ nghĩa có
kiểm soát (semantic catalog) và hệ guardrails. Toàn bộ chạy local-first bằng
Docker Compose. Phạm vi dữ liệu cố định: 2024-01-01 đến 2024-06-30 (2024-H1).

# Cấu trúc báo cáo MỚI gồm 4 chương
Ch.1 Phát biểu bài toán · Ch.2 Cơ sở lý thuyết & công nghệ · Ch.3 Phân tích &
thiết kế · Ch.4 Cài đặt & kiểm thử. Tài liệu đính kèm có thể đánh số chương khác
— hãy BỎ QUA cách đánh số đó, chỉ lấy dữ kiện; báo cáo của tôi dùng đúng 4 chương.

# Quy tắc trình bày
- Văn phong học thuật, trang trọng, ngôi trung tính; KHÔNG dùng "tôi/chúng tôi/em".
- Viết đoạn văn liền mạch là chính; gạch đầu dòng cho danh sách lệnh/endpoint/bước.
- Mỗi mục mở đầu bằng 1–2 câu dẫn nối.
- Chèn code block ngắn cho lệnh tiêu biểu; đề xuất vị trí hình/bảng bằng chú thích
  "Hình 4.y: ..." / "Bảng 4.y: ...".
- Thuật ngữ nhất quán: Bronze/Silver/Gold, ELT, star schema, semantic catalog,
  guardrails, Text-to-SQL, agent.

# Ràng buộc
- KHÔNG thêm tính năng ngoài phạm vi (FHV/HVFHV, streaming, write-agent, cloud).
- KHÔNG bịa số liệu ngoài danh sách "Số liệu thật" bên dưới; cần minh họa thêm
  phải ghi rõ "ví dụ minh họa".

# YÊU CẦU: viết HOÀN CHỈNH "Chương 4 — Cài đặt và kiểm thử"
Phần cài đặt dựa trên Chương 3 báo cáo cũ ĐÃ ÁP DỤNG bản sửa lỗi; phần đánh giá
mở rộng theo cấu trúc dưới.

## Cấu trúc (đánh số 4.1–4.12)
4.1 Môi trường và công nghệ triển khai (Docker Compose 7 service; lệnh khởi chạy).
4.2 Cài đặt pipeline ingestion bằng Airflow (DAG, manifest, atomic+SHA-256, MinIO).
4.3 Cài đặt mô hình hóa dữ liệu bằng dbt (12 model 3 tầng; dbt build; dbt tests).
4.4 Cài đặt lớp ngữ nghĩa và API FastAPI (semantic catalog; 3 endpoint; module).
4.5 Cài đặt AI Agent và guardrails 3 tầng (state machine; sqlglot; repair 1 vòng).
4.6 Cài đặt giao diện Streamlit (4 tab; hiển thị agent_steps).
4.7 Phương pháp kiểm thử & đánh giá (3 trục: chất lượng dữ liệu, hành vi agent,
    hiệu năng; cộng benchmark sinh SQL trên bộ công khai).
4.8 Kết quả chất lượng dữ liệu (dbt tests; lọc Bronze→Silver).
4.9 Kết quả hiệu năng (benchmark P01–P05; latency theo bề mặt).
4.10 Đánh giá AI Agent:
     4.10.1 Bộ test riêng — pass/fail (27 ca: 13 answer + 3 clarification + 11 blocked).
     4.10.2 Độ chính xác sinh SQL trên Spider, so với leaderboard công khai.
4.11 Hạn chế và threats to validity.
4.12 Kết luận chương.

## Số liệu thật (KHÔNG bịa thêm ngoài danh sách này)
- 7 service: minio, airflow-postgres, airflow-init, airflow-webserver,
  airflow-scheduler, api, demo. Lệnh: docker compose up -d (build: --build).
- DAG taxi_monthly_pipeline: chạy ngày 15 hằng tháng, lookback 3 tháng.
- dbt: 12 model = 3 Bronze + 1 Silver + 6 Gold (1 fact + 5 dim) + 2 mart.
  77 dbt tests pass, 2 warn, 0 error.
- Lọc Bronze→Silver (2024-H1): 20.671.900 → 20.354.795 (loại 317.105 ≈ 1,53%);
  null timestamp/zone = 0; negative fare 316.916; pickup ngoài tháng 193.
- API FastAPI: /healthz, /api/v1/schema, /api/v1/query. Engine DuckDB read-only.
- Guardrails 3 tầng: column / table / join. Chỉ 1 câu SELECT; chặn DML/DDL,
  Bronze/Silver, wildcard trên fact_trips, cartesian/sai join; tự giới hạn LIMIT;
  tối đa 1 vòng repair.
- pytest: 44 pass, 2 skipped.
- Đánh giá agent: 27/27 PASS (100%); unsafe_rejection=1.0, grounded=1.0,
  trace_complete=1.0.
- Latency: overall p50 92ms / p95 2472ms; answer p50 753 / p95 2935;
  aggregate_mart p50 715 / p95 1177; star_schema p50 1111 / p95 2935.
- Benchmark API: P01 962ms, P02 1265ms, P03 3701ms, P04 4062ms, P05 1078ms (median).
- [BENCHMARK SPIDER]: ĐIỀN SAU KHI CHẠY — để trống placeholder; sẽ cập nhật EX
  của pipeline (gpt-4o / gpt-4o-mini) và đối chiếu leaderboard.

## Yêu cầu riêng mục 4.10.2 (benchmark sinh SQL)
- Nêu rõ: đây là đánh giá NĂNG LỰC SINH SQL của pipeline trên benchmark công khai
  Spider, chấm bằng script chính thức (Execution Accuracy), so với leaderboard.
- Nêu rõ phạm vi: chỉ module sinh SQL chạy trên Spider; guardrails/planner là đặc
  thù miền taxi nên không thuộc phạm vi Spider (đưa vào threats to validity).
- KHÔNG tuyên bố "tốt hơn SOTA"; trình bày như định vị, vì nhiều hệ leaderboard
  được fine-tune riêng còn đồ án dùng LLM thương mại few-shot.
- Nếu chưa có số Spider, để placeholder bảng và ghi "[số liệu sẽ cập nhật]".

## Yêu cầu trình bày
- Đề xuất vị trí 8 hình minh chứng (Docker, MinIO, Airflow DAG, FastAPI, state
  machine, Streamlit Ask AI, agent trace, guardrail chặn) bằng chú thích Hình 4.y.
- Độ dài: 10–15 trang A4.
```
