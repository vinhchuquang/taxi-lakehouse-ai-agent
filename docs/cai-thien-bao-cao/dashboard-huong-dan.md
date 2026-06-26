# Hướng dẫn dựng & vẽ Bảng điều khiển phân tích (Dashboard) — dữ liệu taxi 2024-H1

Phục vụ Hình `fig:dashboard-ch3` trong `Chuong3-3.tex`. Dashboard lấy dữ liệu từ 2 mart
Gold (`gold_daily_kpis`, `gold_zone_demand`) — đúng nguồn AI Agent đang dùng.

> Lưu ý: `Dashboardv1.png` trong `images/` là dashboard YouTube của project cũ — **không dùng**.

## 1. Bố cục đề xuất (vẽ theo sơ đồ này)

```
┌──────────────────────────────────────────────────────────────┐
│  [Thẻ] Tổng số chuyến   [Thẻ] Tổng cước   [Thẻ] Quãng đường TB │   ← KPI cards
├───────────────────────────────┬──────────────────────────────┤
│ (1) Số chuyến theo tháng       │ (2) Tổng cước theo tháng      │
│     Yellow vs Green (đường)    │     (đường/vùng)              │
├───────────────────────────────┼──────────────────────────────┤
│ (4) Top 10 khu vực đón khách   │ (5) Nhu cầu theo borough      │
│     (cột ngang)                │     (cột)                     │
├───────────────────────────────┼──────────────────────────────┤
│ (3) Quãng đường TB theo loại   │ (6) Tỷ trọng Yellow/Green     │
│     dịch vụ (cột)              │     (tròn/cột)                │
└───────────────────────────────┴──────────────────────────────┘
```

## 2. SQL cho từng panel (DuckDB; đều lọc 2024-H1)

Bộ lọc dùng chung: `WHERE pickup_date >= DATE '2024-01-01' AND pickup_date < DATE '2024-07-01'`

**Thẻ KPI**
```sql
-- Tổng số chuyến
SELECT SUM(trip_count) AS tong_so_chuyen FROM gold_daily_kpis WHERE <loc>;
-- Tổng cước
SELECT SUM(total_fare_amount) AS tong_cuoc FROM gold_daily_kpis WHERE <loc>;
-- Quãng đường trung bình (xấp xỉ)
SELECT AVG(avg_trip_distance) AS quang_duong_tb FROM gold_daily_kpis WHERE <loc>;
```

**(1) Số chuyến theo tháng, tách Yellow/Green** — đường
```sql
SELECT strftime(pickup_date,'%Y-%m') AS month, service_type, SUM(trip_count) AS trip_count
FROM gold_daily_kpis WHERE <loc> GROUP BY 1,2 ORDER BY 1,2;
```
**(2) Tổng cước theo tháng** — đường/vùng
```sql
SELECT strftime(pickup_date,'%Y-%m') AS month, SUM(total_fare_amount) AS total_fare_amount
FROM gold_daily_kpis WHERE <loc> GROUP BY 1 ORDER BY 1;
```
**(3) Quãng đường TB theo loại dịch vụ** — cột
```sql
SELECT service_type, AVG(avg_trip_distance) AS avg_trip_distance
FROM gold_daily_kpis WHERE <loc> GROUP BY 1;
```
**(4) Top 10 khu vực đón khách** — cột ngang
```sql
SELECT zone_name, SUM(trip_count) AS trip_count
FROM gold_zone_demand WHERE <loc> GROUP BY 1 ORDER BY 2 DESC LIMIT 10;
```
**(5) Nhu cầu theo borough** — cột
```sql
SELECT borough, SUM(trip_count) AS trip_count, SUM(total_amount) AS total_amount
FROM gold_zone_demand WHERE <loc> GROUP BY 1 ORDER BY 2 DESC;
```
**(6) Tỷ trọng Yellow/Green** — tròn/cột
```sql
SELECT service_type, SUM(trip_count) AS trip_count
FROM gold_daily_kpis WHERE <loc> GROUP BY 1;
```

> Nếu tên cột `zone_name`/`borough` ở `gold_zone_demand` khác, kiểm tra nhanh ở tab
> **Schema** của Streamlit hoặc `/api/v1/schema`.

## 3. Cách build (khuyến nghị: thêm tab "Dashboard" vào Streamlit)

Trong `services/demo/app.py`, mỗi panel gọi API `/api/v1/query` với SQL ở trên (truyền
kèm `question` bất kỳ + `sql`), rồi vẽ. Khung tối thiểu:

```python
import streamlit as st

C1, C2, C3 = st.columns(3)
C1.metric("Tổng số chuyến", f"{tong_so_chuyen:,}")
C2.metric("Tổng cước", f"{tong_cuoc:,.0f}")
C3.metric("Quãng đường TB (mi)", f"{quang_duong_tb:.2f}")

a, b = st.columns(2)
with a:
    st.subheader("Số chuyến theo tháng")
    st.line_chart(df1.pivot(index="month", columns="service_type", values="trip_count"))
with b:
    st.subheader("Tổng cước theo tháng")
    st.line_chart(df2.set_index("month"))

c, d = st.columns(2)
with c:
    st.subheader("Top khu vực đón khách")
    st.bar_chart(df4.set_index("zone_name"), horizontal=True)
with d:
    st.subheader("Nhu cầu theo borough")
    st.bar_chart(df5.set_index("borough")["trip_count"])

e, f = st.columns(2)
with e:
    st.subheader("Quãng đường TB theo loại")
    st.bar_chart(df3.set_index("service_type"))
with f:
    st.subheader("Tỷ trọng Yellow/Green")
    st.bar_chart(df6.set_index("service_type"))   # st gốc không có pie; dùng bar
```

- Tái dùng hàm gọi API sẵn có trong `app.py` (giống tab SQL) để lấy `df` từ mỗi SQL.
- Biểu đồ tròn (panel 6): Streamlit gốc không có; dùng `st.altair_chart` (Altair `mark_arc`)
  hoặc `plotly`; nếu ngại, để **cột** vẫn đạt yêu cầu.

### Phương án nhanh (không sửa code)
Dùng tab **Charts** hiện có: chạy lần lượt 6 SQL trên, mỗi lần chụp 1 biểu đồ, rồi ghép
6 ảnh thành 1 hình dashboard trong báo cáo. Nhanh nhưng không phải dashboard thật.

## 4. Chụp ảnh cho báo cáo
Sau khi dựng tab Dashboard: mở `http://localhost:8501` → tab **Dashboard** → chụp toàn
màn hình → chèn vào `fig:dashboard-ch3` (thay khung `[CẦN CHÈN HÌNH]`).

---

## 5. Phương án Power BI từ CSV (KHUYẾN NGHỊ — import file, không cần ODBC)

Đây là cách đơn giản nhất để có dashboard Power BI thật cho `fig:dashboard-ch3`.

### B1. Sinh 3 file CSV (script đã có sẵn)
```bash
docker compose up -d
docker compose exec -T api python < scripts/export_gold_powerbi.py
```
Kết quả ghi ra host `warehouse/powerbi_export/` (đã lọc sẵn 2024-H1):

| File CSV | Cột | Dùng cho panel |
|---|---|---|
| `gold_daily_kpis_2024h1.csv` | service_type, pickup_date, trip_count, total_fare_amount, avg_trip_distance | thẻ KPI, (1)(2)(3)(6) |
| `gold_zone_demand_2024h1.csv` | service_type, pickup_date, zone_id, borough, zone_name, trip_count, total_amount | (4)(5) |
| `payment_summary_2024h1.csv` | payment_type, trips, revenue | panel thanh toán (tùy chọn) |

### B2. Nhập vào Power BI Desktop
`Get Data` → `Text/CSV` → chọn từng file → `Load` (3 lần). Sau khi nạp, vào `Model`/`Data`:
- đặt `pickup_date` kiểu **Date**; `trip_count` kiểu **Whole number**; `total_fare_amount`, `avg_trip_distance`, `total_amount`, `revenue` kiểu **Decimal**.

### B3. Tạo cột Tháng (vẽ theo tháng) — tab `Modeling` → `New column` trên bảng daily_kpis
```DAX
Thang = FORMAT('gold_daily_kpis_2024h1'[pickup_date], "YYYY-MM")
```

### B4. Tạo measure — `Modeling` → `New measure`
```DAX
Tong so chuyen = SUM('gold_daily_kpis_2024h1'[trip_count])
Tong cuoc      = SUM('gold_daily_kpis_2024h1'[total_fare_amount])
Quang duong TB = AVERAGE('gold_daily_kpis_2024h1'[avg_trip_distance])
```

### B5. Dựng visual (khớp Bảng `tab:dashboard-panels-ch3` trong Chuong3-3.tex)

| Panel | Visual Power BI | Cấu hình trường |
|---|---|---|
| 3 thẻ KPI | **Card** ×3 | lần lượt measure `Tong so chuyen`, `Tong cuoc`, `Quang duong TB` |
| (1) Số chuyến theo tháng, Yellow/Green | **Line chart** | X=`Thang`, Legend=`service_type`, Y=Sum(`trip_count`) — daily_kpis |
| (2) Tổng cước theo tháng | **Line/Area** | X=`Thang`, Y=Sum(`total_fare_amount`) |
| (3) Quãng đường TB theo loại dịch vụ | **Clustered column** | X=`service_type`, Y=Average(`avg_trip_distance`) |
| (4) Top khu vực đón khách | **Bar (ngang)** | Y=`zone_name`, X=Sum(`trip_count`), Filter `zone_name` = **Top N = 10** by Sum(trip_count) — zone_demand |
| (5) Nhu cầu theo borough | **Clustered column** | X=`borough`, Y=Sum(`trip_count`) — zone_demand |
| (6) Tỷ trọng Yellow/Green | **Pie/Donut** | Legend=`service_type`, Values=Sum(`trip_count`) |
| (tùy chọn) Phân bố thanh toán | **Pie** | Legend=`payment_type`, Values=Sum(`trips`) — payment_summary |

Panel (4) Top 10: kéo `zone_name` vào ô **Filters on this visual** → `Filter type` = `Top N` → `Top` `10` → `By value` = Sum of `trip_count`.

### B6. Sắp xếp + chụp
Bố trí theo sơ đồ ở mục 1 (hàng thẻ KPI trên cùng, 6 biểu đồ 2 cột) → chụp toàn trang → chèn vào `fig:dashboard-ch3` thay khung `[CẦN CHÈN HÌNH]`.

> Số liệu kỳ vọng để đối chiếu (2024-H1): tổng ~20,35 triệu chuyến; Yellow ~98%; Manhattan ~88,7% số chuyến; thẻ tín dụng ~75,4%. Nếu lệch nhiều, kiểm tra lại bộ lọc ngày.
