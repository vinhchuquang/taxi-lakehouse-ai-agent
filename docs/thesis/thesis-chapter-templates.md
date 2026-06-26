# Template viết báo cáo tốt nghiệp (tiếng Việt)

Tài liệu này cung cấp **đoạn văn mẫu** cho từng phần báo cáo. Bạn chỉ cần
**điền vào các chỗ `[ ]`** và chỉnh giọng văn theo phong cách trường yêu cầu.

- Khung tổng thể: xem [thesis-outline.md](thesis-outline.md).
- Thuật ngữ Việt-Anh: xem [glossary.md](glossary.md).
- Hình/bảng tham chiếu: xem [figures-and-tables-index.md](figures-and-tables-index.md).

> Quy ước trong file này:
> - `[X]` = nội dung cần bạn điền cụ thể.
> - `«mô tả»` = chú thích cho người viết, **xóa khi đưa vào báo cáo**.
> - Các số liệu (27/27, 77/2/0, 98M, …) được lấy từ snapshot Phase 37
>   ([agent-evaluation-results.json](../agent-evaluation-results.json)). Nếu chạy
>   lại đánh giá có số khác, cập nhật cả ở đây và trong báo cáo.

---

## CHƯƠNG 1. GIỚI THIỆU

### 1.1 Bối cảnh và động lực

Trong những năm gần đây, khối lượng dữ liệu vận tải đô thị tăng nhanh do
phổ cập thiết bị định vị và công cụ thu thập dữ liệu mở. Cơ quan
*New York City Taxi and Limousine Commission* (TLC) công bố công khai dữ liệu
chuyến đi taxi Yellow và Green theo từng tháng, tổng cộng hàng trăm triệu
chuyến đi mỗi năm. Đây là một tập dữ liệu điển hình cho bài toán **kho dữ liệu
phân tích** (analytics warehouse) ở quy mô vừa: đủ lớn để bộc lộ các vấn đề
thiết kế hệ thống, nhưng vẫn có thể xử lý trên một máy tính cá nhân.

Song song với xu hướng dữ liệu lớn, mô hình kiến trúc **Lakehouse** đã trở
thành lựa chọn tiêu chuẩn cho các hệ thống dữ liệu hiện đại. Lakehouse kết
hợp ưu điểm chi phí thấp của *data lake* với khả năng truy vấn SQL có cấu
trúc của *data warehouse* truyền thống, thông qua mô hình ba lớp
**Bronze → Silver → Gold** [related-work #1, #2].

Một xu hướng thứ hai là **AI agent đọc dữ liệu bằng ngôn ngữ tự nhiên**.
Mặc dù các mô hình ngôn ngữ lớn (LLM) đã chứng minh khả năng sinh truy vấn
SQL từ câu hỏi tự nhiên, việc đưa AI agent vào môi trường phân tích thực tế
gặp ba thách thức chính: (1) tính **an toàn** (không cho phép sửa/xóa dữ
liệu, không lộ dữ liệu thô), (2) tính **chính xác** (truy vấn sinh ra phải
đúng cấu trúc dimensional model), và (3) tính **truy vết** (giải thích được
từng bước agent đã làm).

### 1.2 Mục tiêu đồ án

Đồ án xây dựng một **nền tảng lakehouse local-first cho dữ liệu taxi NYC**,
kèm theo một **AI agent truy vấn chỉ-đọc** trên lớp Gold. Bốn mục tiêu cụ
thể:

1. Xây dựng pipeline ingestion → Bronze → Silver → Gold **lặp lại được** với
   Apache Airflow và dbt.
2. Mô hình hóa lớp Gold theo **star schema Kimball** kèm các aggregate mart
   phục vụ analytics.
3. Triển khai **AI query agent đọc-only** với hệ guardrails ba tầng
   (column, table, join).
4. Đánh giá định lượng độ chính xác, độ an toàn và độ trễ của agent trên một
   bộ test có thể tái lập.

### 1.3 Phạm vi và giới hạn

**Trong phạm vi:**
- Hai nguồn dữ liệu chính: Yellow Taxi và Green Taxi.
- Một nguồn tham chiếu: Taxi Zone Lookup.
- Cửa sổ dữ liệu cố định: từ `2024-01-01` đến `2024-06-30` (gọi là cửa sổ
  bảo vệ `2024-H1`).
- Triển khai local hoàn toàn bằng Docker Compose.
- Agent **chỉ-đọc** trên lớp Gold.

**Ngoài phạm vi (đã được khoanh vùng rõ trong [AGENTS.md](../../AGENTS.md)):**
- Các nguồn FHV, HVFHV (Uber/Lyft).
- Streaming ingestion thời gian thực.
- AI agent có khả năng ghi (write-capable).
- Multi-tenant authentication và phân quyền cấp dòng/cột.
- Triển khai cloud production.

### 1.4 Đóng góp chính

Đồ án đóng góp bốn nội dung chính:

1. **Một lakehouse MVP hoàn chỉnh** chạy local hoàn toàn bằng Docker, có thể
   tái lập trong vài lệnh. Sources, transforms, serving và agent đều được
   đóng gói thành các service độc lập.
2. **Star schema Kimball có kiểm chứng** với 77 dbt tests và phân loại bất
   thường rõ ràng (verified/unverified).
3. **Một read-only agent orchestrator tự xây**, không phụ thuộc các framework
   như LangChain hay Vanna, với ba tầng guardrails (cột, bảng, join) áp dụng
   AST parsing qua thư viện `sqlglot`.
4. **Bộ đánh giá hồi quy 27 trường hợp** gồm 13 câu trả lời đúng,
   3 câu yêu cầu làm rõ và 11 câu bị chặn — đạt 100% PASS, có lưu vết
   JSONL để tái lập.

### 1.5 Cấu trúc báo cáo

Báo cáo gồm sáu chương. Chương 2 trình bày cơ sở lý thuyết về Lakehouse,
dimensional modeling, Text-to-SQL và guardrails. Chương 3 mô tả thiết kế
tổng thể của hệ thống. Chương 4 trình bày chi tiết triển khai. Chương 5
trình bày phương pháp và kết quả đánh giá. Chương 6 tổng kết và đề xuất
hướng phát triển.

---

## CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÁC NGHIÊN CỨU LIÊN QUAN

### 2.1 Kiến trúc Lakehouse

Lakehouse là mô hình kiến trúc dữ liệu kết hợp ưu điểm của data lake (lưu trữ
chi phí thấp trên object storage) và data warehouse (truy vấn SQL có cấu
trúc, ràng buộc và quản trị). Mô hình **medallion** của Databricks
[related-work #1] chia dữ liệu thành ba lớp:

- **Bronze**: dữ liệu thô từ nguồn, lưu nguyên trạng, có thể đọc lại nếu cần
  truy lại nguồn gốc.
- **Silver**: dữ liệu đã chuẩn hóa schema, loại bỏ giá trị không hợp lệ và
  unify giữa các nguồn tương tự.
- **Gold**: dữ liệu phục vụ trực tiếp cho BI và ứng dụng — thường là star
  schema hoặc các aggregate mart.

Đồ án áp dụng đúng mô hình ba lớp này. Khác biệt so với các triển khai
Lakehouse cloud (Databricks, Snowflake) là [TÊN ĐỒ ÁN] dùng **MinIO** làm
object storage và **DuckDB** làm engine truy vấn, cho phép chạy hoàn toàn
trên máy cá nhân mà không cần dịch vụ đám mây.

### 2.2 Dimensional Modeling theo Kimball

Mô hình star schema do Ralph Kimball đề xuất [related-work #4] là tiêu chuẩn
phổ biến cho lớp serving trong data warehouse. Một star schema gồm:

- **Fact table**: bảng sự kiện, mỗi dòng là một biến cố nghiệp vụ (ở đây là
  một chuyến taxi). Lưu các *metric* và các khóa ngoại trỏ tới dimension.
- **Dimension table**: bảng chiều, lưu các thuộc tính mô tả (thời gian, địa
  điểm, loại dịch vụ, …) để slice/dice fact.

Ưu điểm của star schema so với các thiết kế chuẩn hóa (3NF):
- Truy vấn analytical đơn giản, ít JOIN.
- Người dùng nghiệp vụ dễ hiểu.
- Tối ưu cho columnar engine như DuckDB.

«Trong báo cáo, vẽ Hình 2.1: Sơ đồ star schema mẫu (1 fact + 4 dim).»

### 2.3 Modern Data Stack

Đồ án sử dụng "modern data stack" — một bộ các công cụ open-source phối hợp
với nhau:

| Công cụ | Vai trò | Tham khảo |
|---|---|---|
| Apache Airflow | Điều phối DAG ingestion theo lịch | [related-work #6] |
| dbt | Định nghĩa transformation và kiểm thử dữ liệu bằng SQL | [related-work #7] |
| DuckDB | Engine OLAP nhúng, chạy in-process | [related-work #8] |
| MinIO | Object storage tương thích S3 | [related-work #9] |
| FastAPI | Framework Python để xây API agent | [related-work #10] |

### 2.4 Text-to-SQL và AI Agents

Text-to-SQL là bài toán chuyển câu hỏi tự nhiên thành truy vấn SQL. Spider
[related-work #11] là benchmark phổ biến nhất. Các hướng tiếp cận gần đây
dùng LLM (DIN-SQL [related-work #14], SQL-PaLM [related-work #15]) đạt độ
chính xác cao nhưng vẫn gặp vấn đề **hallucination schema** — sinh truy vấn
trên các bảng/cột không tồn tại.

Khung agent (LangChain, LangGraph, Vanna) cung cấp orchestration cho các
luồng "intent → plan → execute". Tuy nhiên các khung này thường ẩn workflow
nội bộ, gây khó khăn khi cần debug và đánh giá định lượng. Vì lý do này,
[TÊN ĐỒ ÁN] **không** dùng các framework đó mà tự xây orchestrator tường
minh — quyết định này được phân tích cụ thể ở Chương 3.

### 2.5 SQL Guardrails

Khi LLM tham gia sinh SQL, việc validate truy vấn trước khi thực thi là bắt
buộc để tránh: (a) phá hủy dữ liệu (DDL/DML), (b) lộ dữ liệu thô (truy vấn
sang lớp Bronze/Silver), (c) JOIN sai gây kết quả nhiễu, (d) prompt injection.

Có hai hướng tiếp cận chính:
- **Deny-list**: liệt kê các pattern cấm. Khó bao quát hết.
- **Allow-list**: chỉ cho phép các pattern đã khai báo trước. An toàn hơn
  nhưng cần định nghĩa rõ ràng schema và join.

Đồ án dùng allow-list dựa trên **semantic catalog** (xem Chương 3) kết hợp
với AST parsing qua `sqlglot` [related-work #20].

### 2.6 Khoảng trống được giải quyết

Tổng hợp lại, đa số nghiên cứu Text-to-SQL hiện nay tập trung vào độ chính
xác trên benchmark, ít đầu tư cho guardrails đủ mạnh phục vụ production. Các
khung agent thương mại lại giấu workflow nội bộ, khó kiểm chứng. Đồ án này
đề xuất một **mô hình tham chiếu nhỏ nhưng đầy đủ**: lakehouse + star schema
+ agent đọc-only với guardrails minh bạch và bộ đánh giá có thể tái lập.

---

## CHƯƠNG 3. THIẾT KẾ HỆ THỐNG

### 3.1 Kiến trúc tổng thể

Hệ thống gồm bảy service đóng gói trong Docker Compose:

1. **`minio`** — object storage lưu Bronze và metadata các lần chạy pipeline.
2. **`airflow-postgres`** — metastore của Airflow.
3. **`airflow-init`** — khởi tạo schema metastore.
4. **`airflow-scheduler`** — chạy DAG.
5. **`airflow-webserver`** — UI quản trị Airflow.
6. **`api`** — FastAPI host AI agent đọc-only.
7. **`demo`** — Streamlit UI cho buổi bảo vệ.

«Chèn Hình 3.1 — Sơ đồ thành phần (Figure 1 trong
[architecture-diagrams.md](architecture-diagrams.md)).»

Luồng dữ liệu tổng quát:
- Airflow lập lịch tải file TLC hàng tháng → MinIO (Bronze).
- dbt đọc Bronze từ MinIO qua DuckDB `httpfs` → build Silver → build Gold
  ngay trong DuckDB.
- FastAPI mở DuckDB ở chế độ read-only và phục vụ agent.
- Streamlit gọi API qua HTTP để hiển thị demo.

«Chèn Hình 3.2 — Luồng Bronze → Silver → Gold.»

### 3.2 Lớp Bronze và Data Contracts

Bronze được thiết kế **immutable**: file nào đã upload thì không sửa, chỉ
thêm. MinIO là *source of truth*; thư mục `data/` local chỉ là cache.

Mỗi lần ingestion thực hiện ba bước:
1. Tải file vào file tạm, kiểm tra kích thước và SHA-256.
2. Atomic promote sang vị trí cuối cùng (đổi tên trong cùng filesystem).
3. Upload lên MinIO kèm metadata SHA-256, kích thước và thời gian tải.

Các đối tượng Bronze đã có sẵn được phân loại **verified** (có metadata
đầy đủ) hoặc **unverified** (file cũ, không có metadata). Phân loại này
được ghi vào pipeline run metadata để dễ truy nguyên.

«Chi tiết contracts: xem [data-contracts.md](../data-contracts.md).»

### 3.3 Lớp Silver — Chuẩn hóa schema

Silver gồm một model duy nhất là `silver_trips_unified`. Model này:

- Đọc `bronze_yellow_trips` và `bronze_green_trips` từ MinIO.
- Map các cột có ý nghĩa giống nhau về tên chuẩn (ví dụ
  `tpep_pickup_datetime` và `lpep_pickup_datetime` đều → `pickup_at`).
- Thêm cột `service_type` để phân biệt Yellow/Green.
- Áp **validity filters**: pickup date trong tháng partition, dropoff sau
  pickup, `total_amount > 0`, `trip_distance` hợp lệ.

Khoảng [X] triệu dòng bị loại bởi validity filters trên toàn bộ cửa sổ
`2024-H1`, được chi tiết hóa trong [data-quality-report.md](../data-quality-report.md).

### 3.4 Lớp Gold — Star Schema

Gold gồm:

**Một fact table**:
- `fact_trips` — mỗi dòng là một chuyến taxi hợp lệ từ Silver.

**Năm dimension table**:
- `dim_date` — ngày, tháng, quý, năm, thứ trong tuần.
- `dim_zone` — vùng (zone), borough, service_zone từ Taxi Zone Lookup.
- `dim_service_type` — `yellow_taxi`, `green_taxi`.
- `dim_vendor` — mã vendor TLC.
- `dim_payment_type` — phương thức thanh toán.

**Hai aggregate mart** (fast path cho câu hỏi phổ biến):
- `gold_daily_kpis` — KPI theo ngày × service_type.
- `gold_zone_demand` — nhu cầu theo cặp pickup/dropoff zone.

«Chi tiết: xem [gold-star-schema.md](../gold-star-schema.md) và
[modeling-decisions.md](../modeling-decisions.md).»

### 3.5 Semantic Catalog

[`contracts/semantic_catalog.yaml`](../../contracts/semantic_catalog.yaml) là
hợp đồng giữa lớp Gold và agent: liệt kê **chính xác** bảng nào, cột nào,
JOIN nào được phép. Mỗi entry có các trường:

- `execution_enabled`: agent có được phép thực thi truy vấn không?
- `columns`: danh sách cột được phép tham chiếu.
- `allowed_joins`: các đường JOIN được phép, ràng buộc bằng cặp cột cụ thể.

Bằng cách tập trung tri thức nghiệp vụ vào một file YAML duy nhất, đồ án
tránh được hai vấn đề: (a) thay đổi schema không đồng bộ giữa các tầng,
(b) agent suy diễn ý nghĩa từ tên cột — dễ sai.

### 3.6 AI Agent Orchestrator

Orchestrator được hiện thực trong
[services/api/app/agent.py](../../services/api/app/agent.py) dưới dạng
**máy trạng thái tường minh** (state machine). Các trạng thái:

1. **Intent Analysis**: phân loại câu hỏi.
2. **Plan**: chọn bảng/cột/filter — ưu tiên deterministic planner, fallback
   LLM.
3. **SQL Generate**: tạo SQL hoặc nhận SQL người dùng cung cấp.
4. **Guardrails Validate**: kiểm tra 3 tầng.
5. **Execute**: thực thi DuckDB read-only với `max_rows`.
6. **Self-check**: so sánh kết quả với mong đợi từ plan.
7. **Answer**: trả deterministic answer + tùy chọn OpenAI synthesis (grounded
   trên rows).

«Chèn Hình 3.3 — State machine agent.»

**Lý do tự xây thay vì dùng LangChain/Vanna:**
- Workflow minh bạch — mỗi bước có thể test và đo riêng.
- Không phụ thuộc abstraction bên thứ ba — giảm nguy cơ thay đổi API.
- Phù hợp phạm vi đồ án (đọc-only, một surface phục vụ).

### 3.7 Hệ Guardrails ba tầng

Mọi SQL sinh ra đều phải qua ba tầng kiểm tra trước khi thực thi:

**Tầng 1 — Column guardrails**
- Chỉ cho phép cột khai báo trong semantic catalog.
- Cấm `SELECT *` trên `fact_trips` (tránh trả về cột không kiểm soát).

**Tầng 2 — Table guardrails**
- Chỉ cho phép bảng có `execution_enabled = true`.
- Chặn truy cập bảng Bronze/Silver.

**Tầng 3 — Join guardrails**
- Chỉ cho phép JOIN có mệnh đề `ON` rõ ràng.
- Chặn cartesian (CROSS JOIN, JOIN không điều kiện).
- Đường JOIN phải khớp với `allowed_joins` trong semantic catalog.

Toàn bộ ba tầng dùng AST parser của `sqlglot` để phân tích SQL — không
dùng regex, tránh các trường hợp né tránh đơn giản (comment, whitespace).

«Chèn Hình 3.4 — Pipeline guardrails.»

---

## CHƯƠNG 4. TRIỂN KHAI

### 4.1 Môi trường

Toàn bộ hệ thống được đóng gói bằng Docker Compose. Quy trình khởi động:

```
docker compose up -d
```

Sau khi container sẵn sàng, người dùng có thể:
- Mở Airflow UI tại `http://localhost:8080`.
- Mở Streamlit demo tại `http://localhost:8501`.
- Gọi API trực tiếp tại `http://localhost:8000`.

«Chi tiết runtime: [runbook.md](../runbook.md).»

### 4.2 Ingestion Pipeline

DAG `taxi_monthly_pipeline` được định nghĩa tại
[airflow/dags/taxi_monthly_pipeline.py](../../airflow/dags/taxi_monthly_pipeline.py).

- Lịch chạy: ngày 15 hàng tháng (TLC công bố trễ ~1 tháng).
- `TLC_LOOKBACK_MONTHS = 3` — kiểm tra lại 3 tháng gần nhất.
- Manual trigger với tham số `{year, month}` để ingest đúng một tháng.

Mỗi lần chạy DAG ghi một file metadata JSON xuống
`metadata/pipeline_runs/taxi_monthly_pipeline/...` trên MinIO. File này
chứa: `run_id`, mode (manual/scheduled), target months, ingestion status,
dbt summary, quality gate.

### 4.3 dbt Models

Tổng cộng 12 models:

| Lớp | Số model | Tên |
|---|---|---|
| Bronze | 3 | `bronze_yellow_trips`, `bronze_green_trips`, `bronze_taxi_zone_lookup` |
| Silver | 1 | `silver_trips_unified` |
| Gold (star) | 6 | `fact_trips`, `dim_date`, `dim_zone`, `dim_service_type`, `dim_vendor`, `dim_payment_type` |
| Gold (mart) | 2 | `gold_daily_kpis`, `gold_zone_demand` |

dbt tests được khai báo trong [dbt/models/schema.yml](../../dbt/models/schema.yml):
77 PASS / 2 WARN / 0 ERROR / 0 SKIP. Hai warning là *anomaly có chủ đích*
(pickup date ngoài tháng partition, 1 dòng KPI bất thường), được phân loại
trong [data-quality-report.md](../data-quality-report.md).

### 4.4 FastAPI Service

Service `api` mở các endpoint:

| Endpoint | Mục đích |
|---|---|
| `/api/v1/schema` | Trả về semantic catalog đã xử lý — agent-visible Gold surface |
| `/api/v1/query` | Nhận câu hỏi tự nhiên hoặc SQL, trả về agent_steps + answer + rows |
| `/healthz` | Healthcheck |

Module chính:
- `agent.py` — orchestrator
- `text_to_sql.py` — deterministic planner + LLM SQL generation
- `sql_guardrails.py` — ba tầng guardrail
- `query_engine.py` — DuckDB executor
- `catalog.py` — loader semantic catalog
- `audit.py` — ghi audit log JSONL

### 4.5 Streamlit Demo

Demo UI có bốn tab:
1. **Schema** — hiển thị các bảng/cột mà agent thấy.
2. **SQL** — chạy SQL trực tiếp.
3. **Ask AI** — hỏi bằng ngôn ngữ tự nhiên, hiển thị `agent_steps`.
4. **Charts** — biểu đồ và export CSV.

«Chèn Hình 4.X — Ảnh chụp Streamlit (chụp lúc đang demo).»

### 4.6 Kiểm thử và CI

- Unit test bằng `pytest`: `python -m pytest -p no:cacheprovider` — kết quả
  44 PASS / 2 SKIP (các test phụ thuộc Docker bị skip trên host).
- Test guardrails và API chạy trong container `api`.
- Test ingestion chạy trên host hoặc container Airflow.

---

## CHƯƠNG 5. ĐÁNH GIÁ

«Toàn bộ chi tiết: xem [evaluation-methodology.md](evaluation-methodology.md).»

### 5.1 Phương pháp đánh giá

Đánh giá được thực hiện trên ba trục:
1. **Chất lượng dữ liệu** — dbt tests.
2. **Tính đúng đắn và an toàn của agent** — bộ 27 cases hồi quy.
3. **Hiệu năng** — đo độ trễ end-to-end.

Tính tái lập được đảm bảo bằng cách: (a) cố định cửa sổ dữ liệu `2024-H1`,
(b) chạy đánh giá trong container `api`, (c) snapshot kết quả ra JSON tại
[agent-evaluation-results.json](../agent-evaluation-results.json).

### 5.2 Chất lượng dữ liệu

dbt build snapshot Phase 25 (`phase25_2024_01_20260506`):
- **77 PASS / 2 WARN / 0 ERROR / 0 SKIP.**
- Hai WARN: `warn_silver_trip_anomalies` (~18K dòng) và
  `warn_gold_metric_anomalies` (1 dòng) — đều là *bất thường nguồn*, đã được
  ghi vào tài liệu chứ không gây thất bại pipeline.

Silver loại khoảng [X] triệu dòng anomaly trên toàn cửa sổ `2024-H1` thông
qua validity filters.

«Chèn Bảng 5.1 — Phân loại dbt tests theo lớp Bronze/Silver/Gold.»

### 5.3 Đánh giá agent

**Tổng quát:** 27/27 cases PASS (100%).

**Phân theo loại:**

| Loại | Số case | Pass | Định nghĩa |
|---|---|---|---|
| answer | 13 | 13 | Câu hỏi hợp lệ, trả về câu trả lời grounded |
| clarification | 3 | 3 | Câu hỏi mơ hồ, agent yêu cầu làm rõ |
| blocked | 11 | 11 | Câu hỏi nguy hiểm/ngoài phạm vi, guardrails chặn |

**Các chỉ số then chốt:**
- `successful_answer_pass_rate` = 1.0
- `unsafe_rejection_rate` = 1.0
- `clarification_pass_rate` = 1.0
- `grounded_answer_rate` = 1.0
- `trace_complete_rate` = 1.0

«Chèn Bảng 5.2 — Chi tiết 11 blocked cases × trục guardrail.»

### 5.4 Hiệu năng

Đo trên 27 cases trong container `api`:

| Chỉ số | Giá trị |
|---|---|
| `overall_p50` | 92 ms |
| `overall_p95` | 2472 ms |
| `answer_p50` | 753 ms |
| `answer_p95` | 2935 ms |
| Aggregate mart (6 case) | p50 715 ms, p95 1177 ms |
| Star schema (7 case) | p50 1111 ms, p95 2935 ms |

Benchmark riêng (Phase 17) trên 5 truy vấn đại diện cho thấy giữ Gold ở dạng
**view** (không materialize thành bảng vật lý) là đủ nhanh cho mục đích đồ
án/demo. Chi tiết: [performance-report.md](../performance-report.md).

### 5.5 Hạn chế và threats to validity

Báo cáo cần nêu rõ năm hạn chế sau:

1. **Selection bias** — Bộ 27 cases do tác giả tự thiết kế từ demo scenarios,
   không phải lấy mẫu từ log người dùng thực.
2. **Không có ground truth bên ngoài** — Độ đúng được kiểm bằng SQL
   deterministic, không có annotator độc lập gán nhãn câu trả lời mong đợi.
3. **Đơn lượt (single-turn)** — Agent không có trạng thái hội thoại; chưa
   đánh giá multi-turn.
4. **Cửa sổ dữ liệu hẹp** — `2024-H1` (6 tháng) so với toàn bộ TLC nhiều năm.
5. **Hardware** — Đo trên máy cá nhân, sẽ khác trong môi trường production
   tải đồng thời.

---

## CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 6.1 Kết quả đạt được

Đồ án đã hoàn thành bốn mục tiêu đề ra ở Chương 1:

1. Pipeline Bronze → Silver → Gold chạy lặp lại được, có metadata bền vững.
2. Star schema Kimball được dựng, 77 dbt tests xanh, anomaly có tài liệu.
3. AI agent đọc-only hoàn chỉnh, có ba tầng guardrails minh bạch, có khả
   năng trace.
4. Bộ đánh giá 27 cases đạt 100% PASS, có snapshot JSON tái lập.

Bằng chứng vật lý: 41 phases được ghi nhật ký trong
[development-roadmap.md](../development-roadmap.md), dataset cố định
`2024-H1`, snapshot đánh giá tại
[agent-evaluation-results.json](../agent-evaluation-results.json).

### 6.2 Hạn chế của đồ án

Như đã nêu ở 5.5, đồ án giới hạn ở phạm vi local, đơn lượt, hai nguồn Yellow
và Green, và đánh giá nội bộ. Đây là sự đánh đổi có chủ đích để hoàn thiện
một MVP hoàn chỉnh thay vì làm nhiều thứ dở dang.

### 6.3 Hướng phát triển

«Chi tiết: [production-roadmap.md](production-roadmap.md).»

Bốn hướng phát triển tiềm năng:

1. **Mở rộng nguồn** — thêm FHV/HVFHV và mở cửa sổ multi-year.
2. **Đánh giá nâng cao** — bộ test adversarial chống prompt injection và
   baseline comparison giữa các biến thể agent.
3. **Multi-turn agent** — thêm conversation store, đánh giá riêng cho
   continuity.
4. **Triển khai production** — Kubernetes, OIDC, monitoring/alerting,
   SLO/SLA chính thức.

---

## Hướng dẫn dùng file này

1. Mở file Word/LaTeX của trường, copy từng section vào theo thứ tự.
2. Tại mỗi `[ ]`, điền số/tên cụ thể.
3. Xóa toàn bộ chú thích `«mô tả»` trước khi nộp.
4. Đối chiếu thuật ngữ với [glossary.md](glossary.md) để dùng nhất quán.
5. Kiểm tra số liệu khớp với
   [agent-evaluation-results.json](../agent-evaluation-results.json) — nếu chạy
   lại đánh giá cho số mới, cập nhật cả file này.
