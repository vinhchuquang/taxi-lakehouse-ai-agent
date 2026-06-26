"""Xuất dữ liệu Gold 2024-H1 ra Parquet + CSV để dựng dashboard Power BI.

Chạy trong container api (đã cấu hình sẵn S3 tới MinIO):
    docker compose exec -T api python < scripts/export_gold_powerbi.py

Kết quả ghi vào /data/warehouse/powerbi_export (hiện trên host ở warehouse/powerbi_export/).
Mở bằng read-only; nếu file chính đang bị khóa thì tự sao chép sang /tmp rồi đọc bản sao
(giữ nguyên tên analytics.duckdb để các view tham chiếu catalog "analytics" hoạt động).
"""

import os
import shutil

import duckdb

DB = "/data/warehouse/analytics.duckdb"
OUT = "/data/warehouse/powerbi_export"
H1 = "pickup_date >= DATE '2024-01-01' and pickup_date < DATE '2024-07-01'"


def connect():
    try:
        c = duckdb.connect(DB, read_only=True)
        c.execute("select 1 from fact_trips limit 1")
        return c
    except duckdb.Error:
        os.makedirs("/tmp/pbexp", exist_ok=True)
        shutil.copy(DB, "/tmp/pbexp/analytics.duckdb")
        return duckdb.connect("/tmp/pbexp/analytics.duckdb", read_only=True)


c = connect()
c.execute("install httpfs")
c.execute("load httpfs")
c.execute("set s3_endpoint = 'minio:9000'")
c.execute("set s3_access_key_id = 'minioadmin'")
c.execute("set s3_secret_access_key = 'minioadmin123'")
c.execute("set s3_region = 'us-east-1'")
c.execute("set s3_url_style = 'path'")
c.execute("set s3_use_ssl = false")

os.makedirs(OUT, exist_ok=True)


def export(name, sql):
    c.execute(f"copy ({sql}) to '{OUT}/{name}.parquet' (format parquet)")
    c.execute(f"copy ({sql}) to '{OUT}/{name}.csv' (header, delimiter ',')")
    n = c.execute(f"select count(*) from ({sql})").fetchone()[0]
    print(f"  {name}: {n} rows -> .parquet + .csv")


print("Exporting Gold 2024-H1 for Power BI ...")
export("gold_daily_kpis_2024h1", f"select * from gold_daily_kpis where {H1}")
export("gold_zone_demand_2024h1", f"select * from gold_zone_demand where {H1}")
export(
    "payment_summary_2024h1",
    f"""select f.payment_type,
               coalesce(d.payment_type_name, 'Unknown') as payment_type_name,
               count(*) as trips,
               round(sum(f.total_amount),2) as revenue
        from fact_trips f
        left join dim_payment_type d on f.payment_type = d.payment_type
        where {H1} group by 1,2 order by 3 desc""",
)
print(f"DONE -> host warehouse/powerbi_export/  {os.listdir(OUT)}")
