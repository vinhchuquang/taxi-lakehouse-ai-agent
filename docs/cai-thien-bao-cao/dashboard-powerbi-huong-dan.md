# Power BI kết nối LIVE tới DuckDB (ODBC) — Dashboard taxi 2024-H1

Power BI nối thẳng vào một **database DuckDB thật** qua **ODBC** (DirectQuery/live), không
xuất file import. Để tránh hai vướng mắc của file warehouse gốc (đang bị API khóa + view khu
vực cần MinIO/S3), ta dùng một **DB serving riêng cho BI** đã materialize sẵn dữ liệu Gold
2024-H1 thành bảng thật, độc lập, read-only.

## 0. DB serving đã tạo sẵn
- File: **`D:\DATN\taxi-lakehouse-ai-agent\warehouse\powerbi.duckdb`** (~1,5 MB)
- Sinh bởi DuckDB 1.5.x trong container `api`. 3 bảng (không phụ thuộc S3):

| Bảng | Dòng | Cột |
|---|---|---|
| `daily_kpis` | 364 | `service_type, pickup_date, trip_count, total_fare_amount, avg_trip_distance` |
| `zone_demand` | 61.154 | `service_type, pickup_date, zone_id, borough, zone_name, trip_count, total_amount` |
| `payment_summary` | 7 | `payment_type, trips, revenue` |

Mã `payment_type`: `1`=Credit card, `2`=Cash, `0`=Other, `3`=No charge, `4`=Dispute, `5`=Unknown.
Lưu ý: `total_fare_amount` là **tiền cước** (không gồm tip/phí); muốn doanh thu gộp dùng
`total_amount` ở `zone_demand`.

**Làm mới số liệu:** chạy lại `docker compose exec -T api python < scripts/build_powerbi_duckdb.py`
rồi **Refresh** trong Power BI (đóng kết nối Power BI trước khi build lại để file không bị khóa).

---

## 1. Cài DuckDB ODBC driver (Windows, một lần)
> Cần quyền Administrator. Yêu cầu sẵn **Microsoft Visual C++ Redistributable** (nếu thiếu sẽ
> báo `VCRUNTIME140.dll` — cài gói VC++ x64 của Microsoft).

1. Tải **Windows x86_64** driver tại: `https://github.com/duckdb/duckdb-odbc/releases`
   → chọn bản **mới nhất** (phải đọc được file tạo bởi DuckDB 1.5.x).
2. Giải nén ra thư mục cố định, ví dụ `C:\duckdb_odbc\` (gồm `duckdb_odbc.dll`,
   `duckdb_odbc_setup.dll`, `odbc_install.exe`).
3. Chuột phải `odbc_install.exe` → **Run as administrator**. Nó tạo registry + một DSN mặc
   định tên `DuckDB` (trỏ `:memory:`).
4. Kiểm tra: Registry `HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI\DuckDB` đã có.

## 2. Tạo DSN trỏ vào file serving (read-only)
1. Mở **ODBC Data Sources (64-bit)** (`odbcad32.exe`) → tab **System DSN** → chọn `DuckDB` →
   **Configure** (hoặc **Add** → DuckDB driver nếu muốn DSN mới tên `taxi_pbi`).
2. Đặt tham số:
   - **database** = `D:\DATN\taxi-lakehouse-ai-agent\warehouse\powerbi.duckdb`
   - **access_mode** = `READ_ONLY`
3. Lưu lại.

## 3. Nối Power BI — 2 cách (chọn 1)

### Cách A (khuyến nghị): Power Query custom connector của MotherDuck — hỗ trợ DirectQuery
1. Tải `duckdb-power-query-connector.mez`:
   `https://github.com/MotherDuck-Open-Source/duckdb-power-query-connector/releases/latest`
2. Chép `.mez` vào `[Documents]\Power BI Desktop\Custom Connectors` (tạo thư mục nếu chưa có).
3. Power BI → **File → Options and settings → Options → Security → Data Extensions** →
   chọn **(Not Recommended) Allow any extension...** → **OK** → khởi động lại Power BI.
4. **Home → Get data → tìm "DuckDB"** → điền hộp thoại:
   - **Database Location** = `D:\DATN\taxi-lakehouse-ai-agent\warehouse\powerbi.duckdb`
   - **MotherDuck Token** = `localtoken`  (bắt buộc gõ chuỗi này cho kết nối local)
   - **Read Only** = `true` ; **Attach_mode** = `single`
5. Chọn **DirectQuery** (kết nối live) → Load. Thấy 3 bảng `daily_kpis`, `zone_demand`,
   `payment_summary`.

### Cách B: ODBC thuần
1. **Home → Get data → ODBC** → chọn DSN `DuckDB` (hoặc `taxi_pbi`) đã cấu hình ở mục 2.
2. Chọn **DirectQuery** → Load 3 bảng.

> DirectQuery: custom connector chỉ cho **một nguồn** ở chế độ DirectQuery (ta chỉ có 1 nên
> ổn). Dữ liệu nhỏ nên **Import** cũng mượt nếu bạn thích.

## 4. Thẻ KPI — New measure (Modeling)
```DAX
Tong so chuyen = SUM(daily_kpis[trip_count])
Tong cuoc USD  = SUM(daily_kpis[total_fare_amount])
Quang duong TB mi =
DIVIDE( SUMX(daily_kpis, daily_kpis[avg_trip_distance]*daily_kpis[trip_count]),
        SUM(daily_kpis[trip_count]) )
```
Cột tháng (New column trên `daily_kpis`): `Thang = FORMAT(daily_kpis[pickup_date], "YYYY-MM")`
Tham chiếu đã kiểm chứng: ~20.354.795 chuyến; cước ~389,6 triệu USD; quãng đường TB ~4,9 mi.

## 5. Sáu panel (bố cục như sơ đồ trong `dashboard-huong-dan.md`)

| # | Panel | Visual | Trường |
|---|---|---|---|
| 1 | Số chuyến theo tháng — Yellow vs Green | Line | Axis `Thang` · Legend `service_type` · Values `Tong so chuyen` |
| 2 | Tổng cước theo tháng | Area | Axis `Thang` · Values `Tong cuoc USD` |
| 3 | Quãng đường TB theo loại | Column | Axis `service_type` · Values `Quang duong TB mi` |
| 4 | Top 10 khu vực đón khách | Bar (ngang) | Axis `zone_name` · Values SUM `trip_count` · Filter Top 10 by `trip_count` |
| 5 | Nhu cầu theo borough | Column | Axis `borough` · Values SUM `trip_count` |
| 6 | Tỷ trọng Yellow/Green | Donut/Pie | Legend `service_type` · Values SUM `trip_count` |

(Bonus) Pie thanh toán: `payment_summary` — Legend `payment_type` (đổi nhãn theo mã), Values `trips`.

## 6. Chụp ảnh cho báo cáo
**View → Page view → Fit to page**, đặt tiêu đề *"Bảng điều khiển phân tích dữ liệu taxi NYC —
nửa đầu 2024"*, chụp toàn trang → chèn vào `fig:dashboard-ch3` (thay `[CẦN CHÈN HÌNH]`).

## 7. Xử lý sự cố
- `VCRUNTIME140.dll is missing` → cài Microsoft VC++ Redistributable x64.
- `Driver not found` → kiểm tra registry `...ODBCINST.INI\DuckDB`; chạy lại `odbc_install.exe`.
- `database created with a different/newer DuckDB version` → tải DuckDB ODBC driver **mới hơn**
  cho khớp DuckDB 1.5.x.
- Build lại file bị `Permission denied/locked` → đóng Power BI (hoặc Refresh xong rồi mới build).
- Custom connector không hiện → bật lại Data Extensions (mục 3.3) và restart Power BI.

---
**Phương án dự phòng (không cần ODBC):** nếu kẹt cài driver, dùng file Parquet/CSV đã xuất ở
`warehouse\powerbi_export\` (script `scripts/export_gold_powerbi.py`) → Power BI **Get data →
Parquet/Folder**. Nhanh nhưng là import, không live.

**Lưu ý báo cáo:** mục Dashboard ở `Chuong3-3.tex` đang mô tả tab Streamlit. Nếu chốt Power BI
qua ODBC live, nhờ AI sửa đoạn đó cho khớp (Power BI ↔ DuckDB serving qua ODBC).

**Nguồn:** [DuckDB ODBC Windows](https://duckdb.org/docs/stable/clients/odbc/windows) ·
[DuckDB ODBC releases](https://github.com/duckdb/duckdb-odbc/releases) ·
[Power BI custom connector (MotherDuck)](https://motherduck.com/docs/integrations/bi-tools/powerbi/powerbi-custom-connector/) ·
[duckdb-power-query-connector](https://github.com/MotherDuck-Open-Source/duckdb-power-query-connector/releases/latest)
