# Handoff — Đồ án "Data Lakehouse + AI Agent Text-to-SQL cho dữ liệu taxi"

Tài liệu bàn giao để một AI khác tiếp tục công việc hoàn thiện **báo cáo tốt nghiệp**
(LaTeX) cho dự án này. Đọc kỹ phần "Ràng buộc" trước khi sửa.

---

## 1. Dự án là gì

- Đồ án tốt nghiệp (ĐH Bách Khoa Hà Nội, Toán–Tin; SV: Chử Quang Vinh, MSSV 20227074).
- Tên: **Thiết kế Data Lakehouse và AI Agent hỗ trợ truy vấn dữ liệu chuyến đi taxi**.
- Nội dung: xây **Data Lakehouse cục bộ** cho dữ liệu NYC TLC **Yellow + Green Taxi**
  (+ Taxi Zone Lookup tham chiếu), tổ chức **Bronze → Silver → Gold**, kèm **AI Agent
  Text-to-SQL CHỈ ĐỌC** truy vấn tầng Gold qua **semantic catalog + guardrails 3 tầng**.
- Chạy **local-first** bằng Docker Compose. **Cửa sổ đánh giá cố định: 2024-H1**
  (2024-01-01 → 2024-06-30) để bảo đảm tái lập.
- Stack: Airflow (điều phối), dbt (mô hình hóa + test), DuckDB (engine OLAP truy vấn),
  MinIO (object storage S3, nguồn Bronze), FastAPI (API chỉ đọc), Streamlit (demo),
  sqlglot (parse/validate SQL cho guardrails), OpenAI API (sinh SQL — tùy chọn),
  PostgreSQL (chỉ là metadata cho Airflow, vai trò OLTP).

## 2. Code dự án (đã hoàn chỉnh, KHÔNG cần sửa cho báo cáo)

- `services/api/app/`: `agent.py` (orchestrator state machine), `text_to_sql.py` (sinh SQL),
  `sql_guardrails.py` (3 tầng: column/table/join), `query_engine.py` (DuckDB read-only),
  `catalog.py`, `audit.py`, `main.py`, `models.py`, `config.py`.
- `services/demo/app.py`: Streamlit (tab Schema/SQL/Ask AI/Charts; chưa có tab Dashboard).
- `dbt/models/`: 12 model (3 Bronze + 1 Silver + 6 Gold = 1 fact + 5 dim, + 2 mart).
- `contracts/semantic_catalog.yaml`: hợp đồng ngữ nghĩa (bảng/cột/join cho phép).
- `airflow/dags/`: DAG `taxi_monthly_pipeline`.
- Scripts: `scripts/agent_eval.py` (đánh giá 27 ca), `scripts/benchmark_phase17.py` (P01–P05),
  `scripts/check_pipeline_run.py`, `scripts/release_check.py`.

## 3. Báo cáo LaTeX — cấu trúc 4 chương

Thư mục: `Đồ_án_TN_ChuQuangVinh_official/`. File `main.tex` `\input` theo thứ tự:

| Chương | Tiêu đề | File `.tex` |
|---|---|---|
| 1 | Phát biểu bài toán | `Chuong1-phat-bieu-bai-toan` |
| 2 | Cơ sở lý thuyết và các thành phần công nghệ | `Chuong2-co-so-ly-thuyet-cong-nghe` |
| 3 | Phân tích và thiết kế hệ thống | `Chuong2-1`, `Chuong3-lap-luan-kien-truc`, `Chuong2-2`, `Chuong2-3`, `Chuong2-4` |
| 4 | Cài đặt và kiểm thử | `Chuong3-1`, `Chuong3-2`, `Chuong3-3`, `Chuong4-phuong-phap-kiem-thu`, `Chuong3-4` |

> Lưu ý đặt tên file gây nhầm: file `Chuong2-*` thực ra thuộc **Chương 3**, file `Chuong3-*`
> thuộc **Chương 4**. Tham chiếu chéo "Chương X" trong văn bản ĐÃ được sửa đúng theo 4 chương
> (đã kiểm: thiết kế = Ch3, cài đặt = Ch4).
> Các file `Chuong1-1..1-6`, `Chuong4-1..4-4`, `Chuong5-1/5-2` là **rác từ bản cũ / project
> khác (giám sát giao dịch gian lận)** — KHÔNG dùng, đã comment trong `main.tex`.

## 4. SỐ LIỆU ĐÃ KIỂM CHỨNG (dùng đúng, KHÔNG bịa)

- **Quy mô kho**: `fact_trips` ~**102 triệu** dòng live, nhưng **báo cáo dùng số bảng đã chốt
  = 98.093.195** (cột "Full warehouse"). Dải ngày: 2023-12 → 2026-03. **Luôn dùng "98 triệu"
  trong báo cáo để khớp bảng, KHÔNG dùng 102 triệu.**
- **2024-H1**: Bronze thô 20.671.900 → Silver hợp lệ **20.354.795** (loại 317.105 ≈ 1,53%;
  negative fare 316.916; pickup ngoài tháng 193; null timestamp/zone = 0).
- **dbt**: 12 model; **77 PASS / 2 WARN / 0 ERROR / 0 SKIP**. 2 WARN =
  `warn_silver_trip_anomalies`, `warn_gold_metric_anomalies` (cảnh báo chất lượng nguồn,
  không chặn build).
- **Đánh giá Agent**: **27/27 PASS** = 13 answer + 3 clarification + 11 blocked;
  unsafe_rejection = grounded = trace_complete = clarification_pass = successful_answer = **1.0**.
- **Độ trễ (ms)**: overall p50 92 / p95 2472; answer p50 753 / p95 2935;
  aggregate_mart p50 715 / p95 1177; star_schema p50 1111 / p95 2935.
- **Benchmark API P01–P05 (median)**: 962 / 1265 / 3701 / 4062 / 1078 ms
  → mart nhanh hơn fact-join ~**3–4 lần** (lập luận giữ Gold 2 lớp).
- **pytest**: 44 passed, 2 skipped. **Guardrails HTTP smoke**: 9/9.
- **Môi trường test**: Windows 11; Python 3.11; DuckDB 1.5.2; sqlglot 30.6.0; pytest 8.3.5
  (nên xác minh lại bằng `docker compose exec api python -V` trước khi trích).
- **7 dịch vụ Docker**: minio, airflow-postgres, airflow-init, airflow-webserver,
  airflow-scheduler, api, demo. DAG `taxi_monthly_pipeline` chạy ngày 15 hằng tháng, lookback 3.

## 5. ĐÃ LÀM (trong các phiên trước)

- Tách 3→4 chương (khung trong `main.tex`).
- Thêm thuyết minh **phạm vi dữ liệu** (toàn kho >98 triệu, đa năm vs đánh giá 2024-H1)
  ở Ch1 (mục Phạm vi) + Ch4 (`Chuong3-2`) — chống ấn tượng "dữ liệu bé".
- Thêm mục **OLTP/OLAP** + bảng so sánh + lý do DuckDB(OLAP)/Postgres(OLTP) (`Chuong2-co-so`).
- Thêm **lập luận hiệu năng** (mart nhanh hơn fact ~3–4×) ở `Chuong3-4`.
- Sửa **bibliography** `main.tex`: Python 3.9→3.11 + thêm DuckDB/MinIO/FastAPI/Streamlit/
  sqlglot/OpenAI/Spider/BIRD.
- Thêm mục **Dashboard** vào `Chuong3-3` + bảng 6 panel + khung hình (hướng dẫn dựng ở
  `docs/cai-thien-bao-cao/dashboard-huong-dan.md`).
- **Gọt văn (rút gọn ~10–15%)** toàn bộ 12 file — giữ nguyên bảng/hình/số liệu (đã kiểm
  `\begin/\end` cân bằng, số liệu nguyên vẹn).
- Đánh dấu mọi khung cần ảnh bằng **`[CẦN CHÈN HÌNH]`** và "Ảnh chụp…".

## 6. CÒN LẠI — ưu tiên theo NỘI DUNG (chất)

1. 🔴 **Viết phần Kết luận** (`main.tex` đang để trống) — kết quả đạt được, hạn chế, hướng
   phát triển; dùng số ở mục 4.
2. 🔴 **Benchmark Spider** (GVHD yêu cầu) — hiện chỉ placeholder. Cách làm: cho **module sinh
   SQL** (`text_to_sql.generate_sql_with_openai`, cấp schema Spider, BỎ guardrails taxi) chạy
   trên **Spider dev**, chấm bằng **script chính thức** (Execution Accuracy), so leaderboard.
   Nêu rõ: chỉ module sinh SQL chạy được trên Spider (guardrails/planner là đặc thù miền taxi
   → đưa vào threats to validity). KHÔNG tuyên bố "tốt hơn SOTA".
3. 🟠 **Mục "Kết quả phân tích 2024-H1" (insight)** — đồ án chưa trình bày phát hiện thực tế
   nào từ dữ liệu. Nên **bật Docker, query kho 2024-H1** (gold_daily_kpis, gold_zone_demand)
   lấy số thật: so sánh Yellow/Green theo tháng, top khu vực đón khách, phân bố thanh toán,
   xu hướng doanh thu → biến hệ thống thành "có giá trị phân tích".
4. 🟠 **Nghiên cứu liên quan (Ch2.7) đào sâu** — hiện chung chung; nêu hệ Text-to-SQL cụ thể
   (DIN-SQL, DAIL-SQL, Spider leaderboard) + lakehouse medallion để làm rõ khoảng trống.
5. 🟠 **Thảo luận sâu phần đánh giá** — phân tích lỗi/ranh giới agent, ý nghĩa 2 anomaly
   warning (chất lượng dữ liệu nguồn TLC), ablation guardrails / deterministic vs LLM.
6. 🟡 **Hình ảnh**: 7 ảnh chụp thật (Docker/MinIO/Airflow/FastAPI/Streamlit/agent trace/
   guardrail) cần người dùng chụp. 4 sơ đồ có thể **vẽ bằng TikZ** (Medallion, OLTP/OLAP,
   state machine agent — đã có TikZ bị comment trong `Chuong2-4`, dashboard) thay vì ảnh.
7. 🟡 **Phụ lục A**: link GitHub đang comment trong `main.tex` (repo
   `github.com/VinhChucomacpro/taxi-lakehouse-ai-agent`) — bật lại + có thể chèn code listing.
8. ⚪ Dọn `references.bib` (block `filecontents`) còn entry Kafka/Spark/Grafana/Faker thừa.
9. ❓ Hỏi người dùng: trường có cần **Tóm tắt tiếng Anh** không (hiện chỉ có tiếng Việt).

## 7. RÀNG BUỘC LÀM VIỆC (quan trọng)

- **Thiếu thông tin / không chắc → HỎI người dùng, KHÔNG tự bịa.** Cần xác minh số liệu/hành
  vi → **bật Docker test lại** (`docker compose up -d`; query qua container `api`:
  `docker compose exec api python -c "import duckdb; c=duckdb.connect('/data/warehouse/analytics.duckdb', read_only=True); ..."`).
- **Văn phong**: học thuật, trang trọng, ngôi trung tính, **KHÔNG "tôi/chúng tôi/em"**, gọn,
  **không lan man**.
- **Không bịa số**; minh họa thêm phải ghi rõ "ví dụ minh họa".
- **Không thêm tính năng ngoài phạm vi**: FHV/HVFHV, streaming, agent ghi dữ liệu, multi-turn,
  cloud production.
- **Người dùng tự compile LaTeX** qua sharelatex (Docker, cổng 8080); họ tự upload file đã sửa.
  → Chỉ cần sửa file `.tex` trên đĩa cho đúng; nếu cần Airflow webserver (cũng cổng 8080) phải
  dừng sharelatex trước.
- Khi sửa `.tex`: KHÔNG đụng nội dung trong `\begin{table}`, `\begin{figure}`, `lstlisting`,
  tikz, `\caption`, `\label`, `\ref`, `\cite`; giữ macro `\path \texttt \textbf \textit`.

## 8. Tài liệu kế hoạch liên quan (trong `docs/cai-thien-bao-cao/`)

- `cai-thien-do-an.md` — danh sách điểm cần cải thiện + trạng thái (A1–A9, B, C, D).
- `ke-hoach-sua-bao-cao-4-chuong.md` — kế hoạch tái cấu trúc + đánh giá agent (Spider).
- `chuong3-sua-loi.md` — bản sửa lỗi (lỗi typo là do trích PDF, .tex đã sạch).
- `pham-vi-du-lieu.md` — đoạn văn + bảng về phạm vi dữ liệu.
- `dashboard-huong-dan.md` — hướng dẫn dựng dashboard (SQL từng panel).
- `00a..04-*.md` — prompt viết từng chương.

## 9. Việc người dùng đang muốn làm tiếp (ưu tiên cao nhất)
Bật Docker lấy số phân tích 2024-H1 → viết mục **"Kết quả phân tích"** + **Kết luận**
(mục 6.1 và 6.3). Đây là phần tăng "chất" nhiều nhất mà AI tự lấy số được.
