# taxi-lakehouse-ai-agent

Đây là repo đồ án xây dựng một nền tảng lakehouse local-first cho dữ liệu taxi
NYC TLC, kèm AI agent read-only để hỏi dữ liệu Gold bằng ngôn ngữ tự nhiên.

## Kiến Trúc

- `MinIO` lưu dữ liệu Bronze dạng object storage.
- `Airflow` điều phối pipeline ingest và transform theo tháng.
- `dbt` xây dựng các lớp `Bronze -> Silver -> Gold` và chạy data tests.
- `DuckDB` lưu warehouse local để phục vụ phân tích, BI và AI query.
- `FastAPI` cung cấp API health, schema và query read-only.
- `OpenAI API` sinh SQL từ câu hỏi tự nhiên.
- `sqlglot` kiểm tra SQL guardrails trước khi chạy.
- `Streamlit` cung cấp giao diện demo AI agent và biểu đồ tự động.

## Cấu Trúc Repo

```text
.
|-- airflow/
|   `-- dags/
|-- contracts/
|-- dbt/
|   `-- models/
|-- docs/
|-- infra/
|-- services/
|   |-- api/
|   `-- demo/
|-- tests/
`-- docker-compose.yml
```

## Phạm Vi Hiện Tại

Đang tập trung vào MVP với:

- `Yellow Taxi` monthly trip parquet
- `Green Taxi` monthly trip parquet
- `Taxi Zone Lookup` làm reference dataset
- pipeline `Bronze -> Silver -> Gold`
- API Text-to-SQL read-only trên Gold
- demo UI bằng Streamlit

Tạm thời chưa đưa vào scope:

- `FHV`
- `HVFHV`
- streaming ingestion
- agent có quyền ghi dữ liệu
- auth/authorization production-grade

## Chạy Local

1. Copy `.env.example` thành `.env` và cập nhật secret nếu cần.
2. Build và chạy stack:

   ```bash
   docker compose up --build
   ```

3. Mở các service:

   - Airflow: `http://localhost:8080`
   - MinIO Console: `http://localhost:9001`
   - API docs: `http://localhost:8000/docs`
   - Streamlit demo: `http://localhost:8501`

Thông tin đăng nhập mặc định:

- Airflow: `admin` / `admin`
- MinIO: xem `MINIO_ROOT_USER` và `MINIO_ROOT_PASSWORD` trong `.env`

## Pipeline Dữ Liệu

Airflow DAG chính: `taxi_monthly_pipeline`.

Luồng xử lý:

1. Tạo manifest cho Yellow, Green và Taxi Zone Lookup.
2. Download file từ TLC CDN vào local mirror dưới `data/`.
3. Upload cùng object key vào bucket MinIO `taxi-lakehouse`.
4. Chạy `dbt build` cho Bronze và Silver.
5. Chạy `dbt build` cho Gold.
6. DuckDB warehouse được lưu dưới `warehouse/analytics.duckdb`.

Object MinIO kỳ vọng:

```text
taxi-lakehouse/
  bronze/yellow_taxi/year=YYYY/month=MM/yellow_tripdata_YYYY-MM.parquet
  bronze/green_taxi/year=YYYY/month=MM/green_tripdata_YYYY-MM.parquet
  reference/taxi_zone_lookup/taxi_zone_lookup.csv
```

## Mô Hình Dữ Liệu

- `Bronze`: đọc raw parquet/csv từ local mirror tương ứng với object đã upload MinIO.
- `Silver`: chuẩn hóa Yellow và Green về schema chung.
- `Gold`: dimensional models và marts phục vụ BI, dashboard và AI agent.

Gold dimensional models hiện có:

- `dim_date`
- `dim_zone`
- `dim_service_type`
- `fact_trips`

Gold marts hiện có:

- `gold_daily_kpis`
- `gold_zone_demand`

Định hướng hiện tại:

- giữ các Gold marts tổng hợp để phục vụ dashboard và AI query ít rủi ro
- `gold_daily_kpis` và `gold_zone_demand` đã build từ dimensional layer
- chưa expose trực tiếp `fact_trips` cho AI cho tới khi semantic catalog có
  metadata đầy đủ về grain, metric và join path an toàn

Silver hiện filter các trip có `pickup_at` nằm ngoài tháng partition của source
file để loại bỏ ngày bất thường.

## AI Query Agent

API chính:

- `GET /healthz`
- `GET /api/v1/schema`
- `POST /api/v1/query`

Guardrails:

- chỉ cho `SELECT`
- chặn DML/DDL
- chỉ cho truy cập bảng Gold trong `contracts/semantic_catalog.yaml`
- ép `LIMIT <= max_rows`
- chạy DuckDB ở chế độ read-only

`/api/v1/query` hỗ trợ hai chế độ:

1. Truyền `question` để OpenAI sinh SQL.
2. Truyền thêm `sql` để test deterministic và demo guardrails.

Ví dụ:

```json
{
  "question": "Show daily trip counts by service type",
  "max_rows": 10,
  "sql": "select service_type, pickup_date, trip_count from gold_daily_kpis order by pickup_date, service_type"
}
```

## Streamlit Demo

Chạy riêng API và demo:

```bash
docker compose up --build api demo
```

Mở:

```text
http://localhost:8501
```

Demo hỗ trợ:

- xem health/schema của API
- hỏi AI bằng ngôn ngữ tự nhiên
- chạy SQL override để test guardrails
- xem SQL đã validate
- tự động vẽ line/bar chart từ kết quả
- cảnh báo kết quả rỗng, chạm limit, metric âm hoặc date range bất thường

## Kiểm Thử

Chạy unit tests:

```bash
python -m pytest -p no:cacheprovider
```

Chạy dbt build trong Airflow container:

```bash
docker compose exec airflow-scheduler python -c "import sys; sys.path.insert(0, '/opt/airflow/dags'); from lib.dbt_runner import run_dbt_build; run_dbt_build()"
```

Trigger DAG với config tháng:

```bash
docker compose exec airflow-scheduler python -c "from airflow.api.common.trigger_dag import trigger_dag; trigger_dag(dag_id='taxi_monthly_pipeline', run_id='e2e_2024_01', conf={'year': 2024, 'month': 1})"
```

Trạng thái verify MVP gần nhất được ghi trong `docs/runbook.md`, mục
`Last Verified MVP State`.

## Tài Liệu Thêm

- `AGENTS.md`: hướng dẫn cho coding agents
- `docs/architecture.md`: kiến trúc tổng quan
- `docs/data-contracts.md`: hợp đồng dữ liệu
- `docs/development-roadmap.md`: hướng phát triển theo giai đoạn
- `docs/modeling-decisions.md`: quyết định mô hình dữ liệu và định hướng dim/fact
- `docs/source-notes.md`: ghi chú nguồn dữ liệu
- `docs/runbook.md`: hướng dẫn vận hành local
