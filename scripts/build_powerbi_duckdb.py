"""Tạo DB DuckDB serving riêng cho Power BI (kết nối live qua ODBC).

Materialize sẵn dữ liệu Gold 2024-H1 thành BẢNG THẬT (không phải view, không phụ thuộc S3,
không đụng lock với API) -> Power BI ODBC trỏ vào file này là đọc live thoải mái.

Chạy trong container api (đã có sẵn credential MinIO):
    docker compose exec -T api python < scripts/build_powerbi_duckdb.py

Kết quả: /data/warehouse/powerbi.duckdb  (host: warehouse/powerbi.duckdb)
Làm mới số liệu: chạy lại script này rồi Refresh trong Power BI.
"""

import os
import shutil

import duckdb

LIVE = "/data/warehouse/analytics.duckdb"
SRC = "/tmp/pbsrc/analytics.duckdb"   # bản sao (giữ tên analytics -> catalog 'analytics')
OUT = "/data/warehouse/powerbi.duckdb"
H1 = "pickup_date >= DATE '2024-01-01' and pickup_date < DATE '2024-07-01'"

# Copy ở mức file luôn được phép dù API đang mở read-only
os.makedirs("/tmp/pbsrc", exist_ok=True)
shutil.copy(LIVE, SRC)

if os.path.exists(OUT):
    os.remove(OUT)

c = duckdb.connect(OUT)  # read-write, file mới
c.execute("install httpfs")
c.execute("load httpfs")
c.execute("set s3_endpoint = 'minio:9000'")
c.execute("set s3_access_key_id = 'minioadmin'")
c.execute("set s3_secret_access_key = 'minioadmin123'")
c.execute("set s3_region = 'us-east-1'")
c.execute("set s3_url_style = 'path'")
c.execute("set s3_use_ssl = false")
c.execute(f"attach '{SRC}' as analytics (read_only)")


def build(name, sql):
    c.execute(f"create or replace table {name} as {sql}")
    n = c.execute(f"select count(*) from {name}").fetchone()[0]
    print(f"  table {name}: {n} rows")


print("Building powerbi.duckdb (serving DB cho Power BI) ...")
build("daily_kpis", f"select * from analytics.main.gold_daily_kpis where {H1}")
build("zone_demand", f"select * from analytics.main.gold_zone_demand where {H1}")
build(
    "payment_summary",
    f"""select payment_type, count(*) as trips,
               round(sum(total_amount),2) as revenue
        from analytics.main.fact_trips where {H1} group by 1 order by 2 desc""",
)
c.execute("detach analytics")
c.close()
print(f"DONE -> host warehouse/powerbi.duckdb  ({os.path.getsize(OUT)/1024/1024:.1f} MB)")
