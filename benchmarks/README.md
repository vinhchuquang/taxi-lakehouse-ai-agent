# Bộ đánh giá (benchmarks)

Đánh giá hệ thống "Data Lakehouse + AI Agent truy vấn taxi". Bốn trục, map thẳng yêu cầu GVHD
và định vị đóng góp **agent truy vấn an toàn + năng lực text-to-SQL cạnh tranh** (không claim vượt SOTA).

Số liệu tổng hợp: [`../docs/cai-thien-bao-cao/ket-qua-danh-gia.md`](../docs/cai-thien-bao-cao/ket-qua-danh-gia.md).

| Thư mục | Trục | Yêu cầu GVHD | Cần gì để chạy |
|---|---|---|---|
| `spider/` | Năng lực text-to-SQL so với hệ khác (Spider) | #1 | Spider data + OpenAI key (image `api`) |
| `taxi/` | Độ chính xác trên domain taxi | #2 | Kho `analytics.duckdb` + MinIO + key (`compose run api`) |
| `safety/` | Tỉ lệ chặn truy vấn nguy hiểm (đóng góp lõi) | — | chỉ catalog (image `api`) |
| `perf/` | Hiệu năng truy vấn lakehouse | #3 | Kho + MinIO (`compose run api`) |

## Chạy

Hầu hết module import `app.*` nên cần chạy trong image `api` (có sẵn `sqlglot`, `openai`, `duckdb`),
với `PYTHONPATH=/work/services/api`. Module chạm tầng zone (`dim_zone`/`gold_zone_demand`) cần MinIO
→ chạy bằng `docker compose run` để vào cùng network.

```bash
# An toàn (nhanh, không cần data/API)
docker run --rm -v "${PWD}:/work" -w /work -e PYTHONPATH=/work/services/api \
  taxi-lakehouse-ai-agent-api:latest python benchmarks/safety/run_safety.py

# Spider — kiểm tra trước (guardrail trên câu gold, không tốn API)
docker run --rm -v "${PWD}:/work" -w /work -e PYTHONPATH=/work/services/api \
  taxi-lakehouse-ai-agent-api:latest python benchmarks/spider/preflight.py \
  --dev spider_data/spider_data/dev.json --tables spider_data/spider_data/tables.json

# Spider — chạy đầy đủ (tốn API)
docker run --rm --env-file .env -v "${PWD}:/work" -w /work -e PYTHONPATH=/work/services/api \
  taxi-lakehouse-ai-agent-api:latest python benchmarks/spider/runner.py \
  --dev spider_data/spider_data/dev.json --tables spider_data/spider_data/tables.json \
  --db-dir spider_data/spider_data/database --mode both --out benchmarks/spider/results_full.json

# Taxi domain + hiệu năng (cần MinIO)
docker compose up -d minio
docker compose run --rm -v "${PWD}:/work" -w /work -e PYTHONPATH=/work/services/api api \
  python benchmarks/taxi/taxi_runner.py --db /work/warehouse/analytics.duckdb
docker compose run --rm -v "${PWD}:/work" -w /work -e PYTHONPATH=/work/services/api api \
  python benchmarks/perf/query_latency.py --db /work/warehouse/analytics.duckdb
```

## Chấm Spider chính danh (so leaderboard)
Sau khi `runner.py` ghi `results_full.pred_wrapped.sql` / `results_full.pred_baseline.sql`,
chấm bằng evaluator chính thức trong `spider/test-suite-sql-eval/` để có EX + exact-match theo
độ khó/thành phần — số đặt cạnh DIN-SQL/DAIL-SQL/C3 được.

## Lưu ý thiết kế (đọc trước khi trích số)
- Spider: bỏ qua planner taxi, chỉ đo LLM + guardrail; chuẩn hóa hoa/thường; join sinh từ FK.
  Chi tiết + các giới hạn guardrail (phép tập hợp, join ngoài FK) trong `spider/README.md`.
- Taxi: chấm theo **chiếu tên cột gold** (chấp nhận agent thừa cột, vẫn chặt về dòng/giá trị/thứ tự).
