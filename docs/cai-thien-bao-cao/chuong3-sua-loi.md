# Danh sách sửa lỗi Chương 3 — "Cài đặt hệ thống"

Đối chiếu `main (14).pdf` với mã nguồn thật trong repo. Mỗi mục ghi rõ **vị trí**,
**tìm** (chuỗi sai) và **thay bằng** (chuỗi đúng). Áp dụng được cho cả Word và LaTeX.

---

## 🔴 A. Lỗi phải sửa (chắc chắn sai)

### A1 — Lặp từ trong tiêu đề mục 3.6.3
- **Tìm:** `3.6.3 Kịch bản kịch bản trình diễn chính`
- **Thay bằng:** `3.6.3 Kịch bản trình diễn chính`

### A2 — Lặp từ ở mục 3.5.4
- **Tìm:** `Bộ bộ kiểm thử guardrails của hệ thống`
- **Thay bằng:** `Bộ kiểm thử guardrails của hệ thống`

### A3 — Sai hoa/thường tên file ở mục 3.4.2 (repo là `agent.py` chữ thường)
- **Tìm:** `Agent.py điều phối toàn bộ quy trình`
- **Thay bằng:** `agent.py điều phối toàn bộ quy trình`

### A4 — Sai hoa trường `agent_steps` ở mục 3.4.2 (đúng là chữ thường)
- **Tìm (lần 1):** `cùng trường Agent_steps`
  - **Thay:** `cùng trường agent_steps`
- **Tìm (lần 2):** `Việc trả về Agent_steps giúp người dùng`
  - **Thay:** `Việc trả về agent_steps giúp người dùng`

### A5 — Sai cú pháp lệnh build ở mục 3.1.1 (dấu cách thừa)
- **Tìm:** `docker compose up -d -- build`
- **Thay bằng:** `docker compose up -d --build`

### A6 — Nhãn dòng sai ở Bảng 3.16
- **Tìm:** `Answer trường hợps`
- **Thay bằng:** `Answer (trả lời)`

---

## 🟠 B. Số liệu & đường dẫn cần chỉnh cho nhất quán

### B1 — Bảng 3.18: tổng các nguyên nhân loại lệch 4 dòng so với tổng loại
316.916 (fare âm) + 193 (pickup ngoài tháng) = 317.109, trong khi tổng loại = 317.105.
Nguyên nhân: một số dòng vi phạm **đồng thời** nhiều bộ lọc. Thêm 1 câu chú thích
ngay dưới Bảng 3.18:

> *Tổng các nguyên nhân loại lớn hơn số dòng bị loại do một số bản ghi vi phạm
> đồng thời nhiều bộ lọc (ví dụ vừa có fare âm vừa nằm ngoài tháng nguồn).*

### B2 — Đường dẫn audit log không nhất quán (mục 3.4.3)
Host mount thực tế: `./warehouse → /data/warehouse`. Trên máy là `warehouse/`,
trong container API là `/data/warehouse/`. Mục 3.1.2 (Bảng 3.4) đã dùng `warehouse/`
cho DuckDB, nên audit log cũng phải dùng `warehouse/`.
- **Tìm:** `dưới dạng JSON Lines tại data/warehouse/query_audit.jsonl`
- **Thay bằng:** `dưới dạng JSON Lines tại warehouse/query_audit.jsonl (tương ứng
  /data/warehouse/query_audit.jsonl bên trong container API)`

### B3 — Bảng 3.8 thiếu `dim_date` (đang có 4/5 dimension)
Hai lựa chọn — chọn 1:
- **Cách 1 (khuyến nghị):** thêm 1 dòng `dim_date` vào Bảng 3.8. Lấy số dòng thật bằng:
  ```bash
  docker compose exec api python -c "import duckdb; c=duckdb.connect('/data/warehouse/analytics.duckdb', read_only=True); print(c.execute('select count(*) from dim_date').fetchone())"
  ```
  Phạm vi 2024-H1 dự kiến = 182 ngày (01/01–30/06/2024, năm nhuận). Cột "Full warehouse"
  điền theo kết quả truy vấn ở trên.
- **Cách 2:** giữ nguyên và thêm chú thích dưới Bảng 3.8: *"Bảng liệt kê các đối tượng
  tiêu biểu; dim_date và bronze_taxi_zone_lookup không đưa vào do số dòng nhỏ/ổn định."*

### B4 — Bảng 3.12: xác minh lại số phiên bản
Chạy trong container `api` để lấy số thật, rồi điền lại nếu lệch:
```bash
docker compose exec api python -V
docker compose exec api python -c "import duckdb, sqlglot; print('duckdb', duckdb.__version__, '| sqlglot', sqlglot.__version__)"
```
Đặc biệt soát lại `Python 3.11.15` và `DuckDB 1.5.2` (nhìn bất thường).

---

## 🟡 C. Văn phong / trình bày (nên sửa cho mượt)

### C1 — Khối "console" pytest ở mục 3.7.2 trộn Việt–Anh
- **Tìm:** `44 kiểm thử, 2 kiểm thử bị bỏ qua in 2.77s`
- **Thay bằng (giữ output gốc):** `44 passed, 2 skipped in 2.77s`

### C2 — Sơ đồ state machine mục 3.5.1 trộn Anh–Việt
- **Tìm:** `Intent Analysis → Lập kế hoạch → SQL Generate → Guardrails → Thực thi → Tự kiểm tra → Tạo câu trả lời`
- **Thay bằng:** `Phân tích ý định → Lập kế hoạch → Sinh SQL → Guardrails → Thực thi → Tự kiểm tra → Tạo câu trả lời`

### C3 — Mục 3.6.2: viết hoa giữa câu trong gạch đầu dòng
- **Tìm:** `thể hiện các bước từ intent, plan, Sinh SQL đến guardrails`
- **Thay bằng:** `thể hiện các bước từ phân tích ý định, lập kế hoạch, sinh SQL đến guardrails`

---

## 🟢 D. Hình ảnh — BẮT BUỘC chèn ảnh thật

Cả 8 hình (3.1–3.8) hiện chỉ có đoạn mô tả "Ảnh chụp màn hình… Nội dung ảnh gồm…",
chưa có ảnh thật. Trước khi nộp phải chèn ảnh chụp thực tế:

| Hình | Ảnh cần chụp |
|---|---|
| 3.1 | `docker compose ps` — 7 service đang chạy/healthy |
| 3.2 | MinIO Console: bucket `taxi-lakehouse` với `bronze/`, `reference/`, `metadata/pipeline_runs/` |
| 3.3 | Airflow UI: DAG `taxi_monthly_pipeline` chạy success |
| 3.4 | FastAPI `http://localhost:8000/docs` hoặc phản hồi `/api/v1/query` |
| 3.5 | Sơ đồ state machine (vẽ hình, không phải ảnh chụp) |
| 3.6 | Streamlit tab Ask AI: câu hỏi + SQL + agent_steps + bảng kết quả |
| 3.7 | Streamlit: agent trace mẫu của một truy vấn thành công |
| 3.8 | Streamlit: guardrail chặn truy vấn (thông báo HTTP 400) |

Gợi ý: sau mỗi đoạn "Ảnh chụp màn hình…" nên thay bằng lệnh chèn ảnh thật
(LaTeX `\includegraphics`, hoặc dán ảnh trong Word) rồi giữ lại caption "Hình 3.x".

---

## 🔵 E. Tài liệu tham khảo (bổ sung cho đủ chất học thuật)

### E1 — Sửa mâu thuẫn phiên bản Python
Ref [3] đang ghi "Python 3.9 Documentation" nhưng hệ thống chạy Python 3.11.
- **Thay:** `Python 3.9 Documentation … https://docs.python.org/3.9/`
- **Bằng:** `Python 3.11 Documentation … https://docs.python.org/3.11/`

### E2 — Thêm trích dẫn cho các công nghệ đã dùng ở Chương 3
Hiện chỉ có 7 mục tham khảo. Nên bổ sung tối thiểu:
- FastAPI — https://fastapi.tiangolo.com/
- DuckDB — https://duckdb.org/docs/
- MinIO — https://min.io/docs/
- Streamlit — https://docs.streamlit.io/
- sqlglot — https://github.com/tobymao/sqlglot
- dbt-duckdb adapter — https://github.com/duckdb/dbt-duckdb
- OpenAI API — https://platform.openai.com/docs/

---

## Thứ tự ưu tiên xử lý
1. Nhóm A (6 lỗi find/replace) — sửa ngay, 5 phút.
2. Nhóm D — chèn ảnh thật (quan trọng nhất với hội đồng).
3. Nhóm B — chỉnh số liệu/đường dẫn + chạy 2 lệnh xác minh phiên bản & dim_date.
4. Nhóm C, E — đánh bóng văn phong và tham khảo.
