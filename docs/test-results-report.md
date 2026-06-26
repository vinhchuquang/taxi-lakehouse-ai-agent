# Báo Cáo Kết Quả Kiểm Thử

**Ngày thực hiện:** 2026-05-22  
**Môi trường:** Windows 11, Python 3.11.2, pytest 8.3.5; Docker stack (api, demo, airflow, minio)  
**Dataset kiểm thử:** NYC TLC Taxi 2024-H1 (`2024-01-01` – `2024-06-30`)

---

## 1. Tổng Quan

Hệ thống được kiểm thử trên 4 tầng, bao gồm cả Docker runtime:

| Tầng kiểm thử | Công cụ | Số test case | Kết quả |
|---|---|---:|---|
| Unit tests (host Python) | pytest 8.3.5 | 44 passed / 2 skipped | **PASS** |
| Guardrail smoke tests (Docker API live) | HTTP / PowerShell | 9 cases | **9/9 PASS** |
| Kiểm thử tích hợp AI agent (Docker API live) | `scripts/agent_eval.py` | 27 cases | **27/27 PASS** |
| Kiểm thử chất lượng pipeline | `scripts/release_check.py` + `check_pipeline_run.py` | — | **PASS** |

**Trạng thái Docker stack:**

| Service | URL | Trạng thái |
|---|---|---|
| FastAPI | `http://localhost:8000` | `status=ok`, DuckDB connectable, catalog loaded |
| Streamlit demo | `http://localhost:8501` | HTTP 200 |
| Airflow | `http://localhost:8080` | metadatabase healthy, scheduler healthy |
| MinIO | `http://localhost:9001` | running |

> **Ghi chú về 2 test bị skip:** `test_sql_guardrails.py` và `test_api_smoke.py` yêu cầu `sqlglot` và `duckdb` trên host Python. Hai thư viện này chỉ tồn tại trong Docker `api` container. Thay vào đó, guardrail được kiểm chứng trực tiếp qua HTTP smoke tests (xem Mục 4).

---

## 2. Kết Quả Unit Tests

**Lệnh chạy:**
```bash
python -m pytest -p no:cacheprovider -v
```

**Kết quả tổng hợp:**
```
44 passed, 2 skipped in 2.77s
```

### 2.1 Nhóm test theo module

#### `test_tlc_ingestion.py` — Kiểm thử ingestion pipeline (18 tests)

| Test | Mô tả | Kết quả |
|---|---|---|
| `test_build_tripdata_url_for_yellow` | Tạo đúng URL TLC cho Yellow Taxi | PASS |
| `test_build_trip_manifest_for_green` | Tạo manifest tháng đúng cho Green Taxi | PASS |
| `test_month_start_with_lag_handles_same_year` | Tính tháng lookback trong cùng năm | PASS |
| `test_month_start_with_lag_handles_year_boundary` | Tính tháng lookback qua ranh giới năm | PASS |
| `test_month_start_with_lag_rejects_negative_lag` | Từ chối lag âm | PASS |
| `test_previous_month_starts_returns_oldest_to_newest` | Thứ tự tháng từ cũ đến mới | PASS |
| `test_previous_month_starts_rejects_non_positive_count` | Từ chối count không dương | PASS |
| `test_is_historical_missing_source_uses_publication_grace` | Phân loại nguồn lịch sử thiếu | PASS |
| `test_build_lookup_manifest` | Tạo manifest Taxi Zone Lookup | PASS |
| `test_download_file_to_local_uses_atomic_temp_file` | Download atomic qua temp file | PASS |
| `test_download_file_to_local_preserves_existing_file_on_failure` | Giữ file cũ nếu download lỗi | PASS |
| `test_upload_local_file_to_minio_creates_bucket_and_uploads` | Upload lên MinIO, tạo bucket nếu chưa có | PASS |
| `test_upload_local_file_to_minio_rejects_empty_file` | Từ chối upload file rỗng | PASS |
| `test_ingest_file_to_minio_skips_existing_object` | Bỏ qua object đã tồn tại (có metadata) | PASS |
| `test_ingest_file_to_minio_skips_existing_object_without_metadata` | Bỏ qua object tồn tại (không có metadata) | PASS |
| `test_ingest_file_to_minio_rejects_existing_metadata_size_mismatch` | Từ chối object bị thay đổi kích thước | PASS |
| `test_ingest_file_to_minio_skips_unpublished_source` | Bỏ qua nguồn TLC chưa công bố (HTTP 403/404) | PASS |
| `test_ingest_file_to_minio_marks_historical_missing_source` | Đánh dấu nguồn lịch sử bị thiếu | PASS |

#### `test_pipeline_metadata.py` — Kiểm thử metadata pipeline (6 tests)

| Test | Mô tả | Kết quả |
|---|---|---|
| `test_pipeline_run_metadata_key_is_stable` | Key metadata MinIO ổn định theo run-id | PASS |
| `test_build_pipeline_run_summary_is_json_serializable` | Summary pipeline có thể serialize JSON | PASS |
| `test_quality_gate_marks_warnings_for_review` | Quality gate phân loại cảnh báo đúng | PASS |
| `test_quality_gate_marks_blocking_ingestion_failure` | Quality gate chặn lỗi ingestion nghiêm trọng | PASS |
| `test_write_pipeline_run_summary_local` | Ghi summary ra file local | PASS |
| `test_upload_pipeline_run_summary_to_minio_puts_json_object` | Upload summary JSON lên MinIO | PASS |

#### `test_semantic_catalog.py` — Kiểm thử semantic catalog và AI planner (10 tests)

| Test | Mô tả | Kết quả |
|---|---|---|
| `test_semantic_catalog_has_tables` | Catalog chứa đầy đủ các bảng Gold | PASS |
| `test_semantic_catalog_describes_gold_star_schema_and_execution_surface` | Mô tả star schema và execution flags | PASS |
| `test_catalog_loader_and_prompt_include_semantic_metadata` | Loader và prompt chứa metadata ngữ nghĩa | PASS |
| `test_prompt_can_render_star_schema_planning_context` | Render context cho star-schema planning | PASS |
| `test_common_vietnamese_monthly_service_comparison_uses_daily_kpi_mart` | Câu hỏi tiếng Việt về so sánh tháng → `gold_daily_kpis` | PASS |
| `test_vietnamese_h1_demo_prompt_uses_daily_kpi_mart` | Demo H1 tiếng Việt → `gold_daily_kpis` | PASS |
| `test_planner_generates_monthly_service_distance_from_daily_kpis` | Khoảng cách tháng → `gold_daily_kpis` | PASS |
| `test_planner_generates_monthly_service_total_amount_from_fact` | Tổng tiền tháng → `fact_trips` | PASS |
| `test_planner_generates_vendor_monthly_trend_with_allowed_joins` | Phân tích vendor → join hợp lệ | PASS |
| `test_planner_generates_pickup_dropoff_borough_comparison` | So sánh quận đón/trả → join đúng vai trò | PASS |

#### `test_dbt_runner.py` — Kiểm thử dbt runner (5 tests)

| Test | Mô tả | Kết quả |
|---|---|---|
| `test_ensure_dbt_profile_writes_expected_profile` | Profile dbt ghi đúng cấu hình | PASS |
| `test_bronze_models_default_to_minio_paths` | Bronze models đọc từ MinIO S3 paths | PASS |
| `test_dbt_project_configures_minio_access_on_run_start` | Cấu hình `httpfs`/S3 trước khi build | PASS |
| `test_summarize_run_results_counts_statuses` | Đếm đúng pass/warn/error/skip từ `run_results.json` | PASS |
| `test_run_dbt_build_returns_summary` | Trả về summary sau dbt build | PASS |

#### `test_operational_scripts.py` — Kiểm thử scripts vận hành (5 tests)

| Test | Mô tả | Kết quả |
|---|---|---|
| `test_check_pipeline_run_validates_summary` | Script xác nhận summary hợp lệ | PASS |
| `test_check_pipeline_run_detects_missing_quality_counts` | Phát hiện thiếu quality count | PASS |
| `test_check_pipeline_run_finds_metadata_by_run_id` | Tìm metadata theo run-id | PASS |
| `test_agent_eval_detects_expected_planning_payload` | Eval script kiểm tra planning payload | PASS |
| `test_agent_eval_cases_include_bilingual_and_guardrail_coverage` | Eval bao phủ câu hỏi song ngữ và guardrail | PASS |

#### Tests bị skip (dependency-gated)

| Module | Lý do skip | Môi trường kiểm chứng |
|---|---|---|
| `test_sql_guardrails.py` | `No module named 'sqlglot'` trên host | Docker `api` container |
| `test_api_smoke.py` | `No module named 'duckdb'` trên host | Docker `api` container |

---

## 3. Kiểm Thử AI Agent (Regression Harness)

**Lệnh chạy** (yêu cầu Docker stack đang chạy):
```bash
python scripts/agent_eval.py --base-url http://localhost:8000 --window 2024-H1 \
    --output docs/agent-evaluation-results.json
```

**Kết quả:** `27/27 PASS`

### 3.1 Tổng hợp theo loại

| Loại test | Số case | Pass | Tỷ lệ |
|---|---:|---:|---:|
| Trả lời thành công (`answer`) | 13 | 13 | 100% |
| Yêu cầu làm rõ (`clarification`) | 3 | 3 | 100% |
| Chặn truy vấn nguy hiểm (`blocked`) | 11 | 11 | 100% |
| **Tổng** | **27** | **27** | **100%** |

### 3.2 Chỉ số chất lượng agent

| Chỉ số | Giá trị |
|---|---|
| Tỷ lệ trả lời đúng (`answer pass rate`) | 1.0 (100%) |
| Tỷ lệ từ chối truy vấn không an toàn (`unsafe rejection rate`) | 1.0 (100%) |
| Tỷ lệ yêu cầu làm rõ đúng (`clarification pass rate`) | 1.0 (100%) |
| Tỷ lệ trace đầy đủ (`trace completeness rate`) | 1.0 (100%) |
| Tỷ lệ câu trả lời có căn cứ (`grounded answer rate`) | 1.0 (100%) |

### 3.3 Độ trễ phản hồi (latency)

| Bề mặt truy vấn | Số case | P50 (ms) | P95 (ms) |
|---|---:|---:|---:|
| Aggregate mart (`gold_daily_kpis`, `gold_zone_demand`) | 6 | 715 | 1177 |
| Star schema (`fact_trips` + dimensions) | 7 | 1111 | 2935 |
| **Tổng answer cases** | **13** | **753** | **2935** |
| Overall (bao gồm clarification, blocked) | 27 | 92 | 2472 |

### 3.4 Chi tiết các case trả lời thành công

| Case | Bề mặt | Bảng sử dụng | Số hàng | Latency (ms) |
|---|---|---|---:|---:|
| A01 | aggregate_mart | `gold_daily_kpis` | 12 | 475 |
| A02 | aggregate_mart | `gold_daily_kpis` | 12 | 740 |
| A03 | aggregate_mart | `gold_daily_kpis` | 12 | 671 |
| A04 | star_schema | `fact_trips` | 12 | 675 |
| A05 | star_schema | `fact_trips`, `dim_vendor` | 17 | 1111 |
| A06 | star_schema | `fact_trips`, `dim_payment_type` | 6 | 2935 |
| A07 | aggregate_mart | `gold_zone_demand` | 8 | 1177 |
| A08 | star_schema | `fact_trips`, `dim_zone` | 50 | 1035 |
| A09 | aggregate_mart | `gold_zone_demand` | 50 | 753 |
| A10 | star_schema | `fact_trips`, `dim_zone` | 8 | 634 |
| A11 | star_schema | `fact_trips`, `dim_date` | 6 | 1246 |
| A12 | star_schema | `fact_trips`, `dim_vendor` | 3 | 2472 |
| A13 | aggregate_mart | `gold_zone_demand` | 8 | 690 |

### 3.5 Chi tiết các case bị chặn (guardrails)

| Case | Loại vi phạm | Thông báo lỗi | HTTP Status |
|---|---|---|---|
| B01 | DML/DDL | `Only SELECT queries are allowed.` | 400 |
| B02 | Wildcard trên fact table | `Wildcard SELECT is not allowed for detailed Gold tables: fact_trips.` | 400 |
| B03 | Truy cập Bronze | `Query references non-Gold or unknown tables: bronze_yellow_trips.` | 400 |
| B04 | Truy cập Silver | `Query references non-Gold or unknown tables: silver_trips_unified.` | 400 |
| B05 | Bảng không tồn tại | `Query references non-Gold or unknown tables: gold_unknown.` | 400 |
| B06 | Cột không tồn tại | `Query references unknown column: fake_metric.` | 400 |
| B07 | Join không hợp lệ | `JOIN condition does not match an allowed semantic catalog join path.` | 400 |
| B08 | JOIN thiếu ON | `JOIN must include an ON condition.` | 400 |
| B09 | Cartesian JOIN | `Cartesian or CROSS JOIN is not allowed.` | 400 |
| B10 | DML (INSERT) | `Only SELECT queries are allowed.` | 400 |
| B11 | Không tham chiếu bảng Gold | `Query must reference at least one curated Gold table.` | 400 |

---

## 4. Kiểm Thử Guardrail Qua HTTP (Docker Live)

**Điều kiện:** Docker stack đang chạy, API `http://localhost:8000` healthy.

**Kết quả:** `9/9 PASS`

| Case | Loại | SQL mẫu | HTTP Status | Kết quả |
|---|---|---|---|---|
| `valid_mart_kpis` | Truy vấn hợp lệ | `SELECT ... FROM gold_daily_kpis` | 200 (5 rows) | PASS |
| `valid_fact_vendor` | Truy vấn hợp lệ | `SELECT ... FROM fact_trips JOIN dim_vendor ON ...` | 200 (3 rows) | PASS |
| `block_ddl` | Chặn DDL | `DROP TABLE gold_daily_kpis` | 400 | PASS |
| `block_wildcard` | Chặn wildcard | `SELECT * FROM fact_trips` | 400 | PASS |
| `block_silver` | Chặn Silver | `SELECT * FROM silver_trips_unified` | 400 | PASS |
| `block_bronze` | Chặn Bronze | `SELECT * FROM bronze_yellow_trips` | 400 | PASS |
| `block_bad_col` | Cột không tồn tại | `SELECT fake_metric FROM gold_daily_kpis` | 400 | PASS |
| `block_cross_join` | CROSS JOIN | `... CROSS JOIN dim_vendor` | 400 | PASS |
| `block_no_on` | JOIN thiếu ON | `... JOIN dim_vendor LIMIT 5` | 400 | PASS |

---

## 5. Kiểm Thử Pipeline Metadata (Host)

**Lệnh chạy:**
```bash
python scripts/check_pipeline_run.py --run-id phase25_2024_01_20260506 --local-only
```

**Kết quả:**
```
Pipeline metadata check passed.
- data\metadata\pipeline_runs\taxi_monthly_pipeline\2026-03-15\
  phase25_2024_01_20260506.json:
  mode=manual  months=['2024-01']  quality=passed_with_warnings
  dbt={'error': 0, 'pass': 77, 'skip': 0, 'warn': 2}
```

| Trường kiểm tra | Giá trị |
|---|---|
| Run mode | `manual` |
| Target months | `['2024-01']` |
| Quality gate | `passed_with_warnings` |
| dbt pass | 77 |
| dbt warn | 2 (warning-only anomaly tests — không phải lỗi chặn) |
| dbt error | 0 |
| dbt skip | 0 |

---

## 5. Kiểm Thử Release Hygiene

**Lệnh chạy:**
```bash
python scripts/release_check.py
```

**Kết quả:**
```
Release check passed.
```

Bao gồm kiểm tra:
- Không có file `dbt/target` bị track trong git
- Không có secret được commit
- Tất cả Gold model trong `dbt/models/gold/` đều có entry trong `contracts/semantic_catalog.yaml`

---

## 6. Hiệu Năng API (Benchmark Phase 17)

Benchmark đo thời gian phản hồi end-to-end qua API path đầy đủ (SQL validation → DuckDB execution → audit logging). Dataset: `2024-H1`.

| Case | Truy vấn | Bề mặt | Số hàng | Median (ms) | Min (ms) | Max (ms) |
|---|---|---|---:|---:|---:|---:|
| P01 | Daily KPI trend | `gold_daily_kpis` | 364 | 962 | 914 | 2999 |
| P02 | Zone demand ranking | `gold_zone_demand` | 25 | 1265 | 1171 | 1415 |
| P03 | Vendor aggregation | `fact_trips` + `dim_vendor` | 3 | 3701 | 3348 | 4820 |
| P04 | Payment-type aggregation | `fact_trips` + `dim_payment_type` | 6 | 4062 | 3347 | 4416 |
| P05 | Pickup/dropoff zone joins | `fact_trips` + 2× `dim_zone` | 50 | 1078 | 1062 | 1256 |

**Nhận xét:**
- Aggregate mart (P01, P02) phản hồi dưới 1.3 giây — phù hợp cho demo tương tác.
- Star-schema join với vendor/payment (P03, P04) mất 3–4 giây do quét toàn bộ fact rows; chấp nhận được với dữ liệu 6 tháng.
- Không thay đổi materialization vì latency hiện tại đáp ứng yêu cầu demo.

---

## 7. Chất Lượng Dữ Liệu (Defense Window 2024-H1)

Dbt build verification: `PASS=77, WARN=2, ERROR=0, SKIP=0` (ghi nhận 2026-05-06).

| Tầng | Tổng hàng (full warehouse) | Hàng trong 2024-H1 |
|---|---:|---:|
| Bronze Yellow Taxi | 100,393,644 | 20,332,093 |
| Bronze Green Taxi | 1,393,453 | 339,807 |
| Silver trips unified | 98,093,195 | 20,354,795 |
| fact_trips | 98,093,195 | 20,354,795 |
| gold_daily_kpis | 1,642 | 364 |
| gold_zone_demand | 283,947 | 61,154 |
| dim_zone | 265 | 265 (reference) |
| dim_service_type | 2 | 2 |
| dim_vendor | 4 | 4 |
| dim_payment_type | 6 | 6 |

**Bronze → Silver filtering (2024-H1):**

| Kiểm tra | Hàng |
|---|---:|
| Raw Bronze rows | 20,671,900 |
| Rows qua Silver filters | 20,354,795 |
| Rows bị loại | 317,105 |
| Null pickup/dropoff timestamp | 0 |
| Null pickup/dropoff zone | 0 |
| Negative trip distance | 0 |

---

## 8. Môi Trường Kiểm Thử

| Thành phần | Phiên bản |
|---|---|
| Python (host) | 3.11.2 (Windows, MSC v.1934 64-bit) |
| Python (API container) | 3.11.15 (Linux) |
| pytest (host) | 8.3.5 |
| OS | Windows 11 Home 10.0.26200 |
| Docker stack | docker compose (images pre-built) |
| sqlglot | 30.6.0 (Docker `api` container) |
| duckdb | 1.5.2 (Docker `api` container) |
| FastAPI | `http://localhost:8000` — `status=ok`, catalog loaded |
| Airflow | `http://localhost:8080` — scheduler healthy |
| MinIO | `http://localhost:9001` — running |
| Streamlit | `http://localhost:8501` — HTTP 200 |

---

## 9. Kết Luận

Toàn bộ test suite host-local vượt qua với **44 passed, 2 skipped**. Hai test bị skip là do thiếu dependency runtime trên host Python (`sqlglot`, `duckdb`) — không phải lỗi code — và đã được kiểm chứng trực tiếp qua **9/9 HTTP guardrail smoke tests** trên Docker API live.

AI agent regression harness chạy trực tiếp trên Docker stack đạt **27/27 cases (100%)** trên tất cả ba loại: trả lời thành công (13 cases), yêu cầu làm rõ (3 cases), và từ chối truy vấn nguy hiểm (11 cases). Tất cả guardrails — DDL, wildcard, Bronze/Silver access, cột không hợp lệ, join sai — đều hoạt động đúng.

Pipeline metadata, release hygiene, và dbt build evidence đều ở trạng thái **PASS**. Docker stack (API, Streamlit, Airflow, MinIO) hoạt động ổn định trong lần kiểm thử ngày 2026-05-22.
