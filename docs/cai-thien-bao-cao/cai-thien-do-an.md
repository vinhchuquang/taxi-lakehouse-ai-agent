# Những điểm cần cải thiện đồ án

Tổng hợp các việc cần làm để hoàn thiện báo cáo & đồ án trước bảo vệ, gom từ góp ý
của GVHD và các lần rà soát. Mỗi mục ghi rõ trạng thái và file chi tiết liên quan.

> Tài liệu liên quan:
> - Kế hoạch tái cấu trúc 4 chương: [ke-hoach-sua-bao-cao-4-chuong.md](ke-hoach-sua-bao-cao-4-chuong.md)
> - Bản sửa lỗi chương cài đặt (viết theo bản PDF cũ; nội dung này nay là **Chương 4**, hình đánh số **4.x**): [chuong3-sua-loi.md](chuong3-sua-loi.md)
> - Phương pháp đánh giá hiện có: [thesis/evaluation-methodology.md](../thesis/evaluation-methodology.md)

---

## A. Cấu trúc & nội dung báo cáo

> Cập nhật theo **cấu trúc 4 chương mới** đã dựng trong `main.tex`:
> Ch.1 Phát biểu bài toán · Ch.2 Cơ sở lý thuyết & công nghệ · Ch.3 Phân tích & thiết kế ·
> Ch.4 Cài đặt & kiểm thử. (Phần "Cài đặt" trước đây là Chương 3 nay là **Chương 4**.)

| # | Việc | Trạng thái | Chi tiết |
|---|---|---|---|
| A1 | Tách báo cáo **3 → 4 chương** | ✅ **Đã làm** | `main.tex` đã có khung 4 chương + `\input` đúng thứ tự |
| A2 | Sửa lỗi typo chương cài đặt (lặp từ, `agent.py`, `--build`, đường dẫn audit, nhãn bảng) | ✅ **Không cần** | Đã kiểm chứng: các lỗi đó **chỉ là lỗi trích xuất PDF**, file `.tex` đã sạch |
| A3 | **Chèn ảnh thật** cho các khung placeholder | ⏳ **Chưa** (cần ảnh) | 9 khung: 8 ảnh chụp ở Chương 4 (Hình 4.x) + sơ đồ Medallion (Ch.2) + luồng AI Agent (Ch.3). Tìm bằng `[CẦN CHÈN HÌNH]` và `Ảnh chụp` |
| A4 | **Lập luận lựa chọn kiến trúc + số liệu** (mart nhanh hơn fact ~3–4×) | ✅ **Đã làm** | `Chuong3-4.tex` (sau bảng benchmark) + `Chuong3-lap-luan-kien-truc.tex` |
| A5 | **Tài liệu tham khảo**: Python 3.9→3.11 + thêm DuckDB/MinIO/FastAPI/Streamlit/sqlglot/OpenAI/Spider/BIRD | ✅ **Đã làm** | `main.tex` khối `thebibliography` |
| A6 | **Phạm vi dữ liệu** (toàn kho vs 2024-H1) chống ấn tượng "dữ liệu bé" | ✅ **Đã làm** | `Chuong1` mục Phạm vi + `Chuong3-2` (dùng số **>98 triệu** theo bảng đã chốt; kho live ~102 triệu) — [pham-vi-du-lieu.md](pham-vi-du-lieu.md) |
| A7 | **Mục OLTP/OLAP** + bảng so sánh + lý do chọn DuckDB(OLAP)/Postgres(OLTP) | ✅ **Đã làm** | `Chuong2-co-so-ly-thuyet-cong-nghe.tex` (mục mới) |
| A8 | **Viết phần Kết luận** cho đề tài taxi | 🔴 **Chưa** | `main.tex` đang để trống; `Chuong5-1/5-2.tex` là kết luận project CŨ (lạc đề, đã comment) — cần viết mới |
| A9 | **Phụ lục A (Mã nguồn)**: bỏ comment link GitHub | 🟠 **Chưa** | `main.tex` dòng link repo đang bị comment |

---

## B. Đánh giá AI Agent — phần TRỌNG TÂM thầy yêu cầu

Thầy yêu cầu 2 việc: (1) test trên **bộ công khai có leaderboard**, so tỷ lệ sinh SQL với
người ngoài; (2) trên **bộ test riêng** xem pass/fail.

### B1. Benchmark trên bộ công khai (Spider) — so với leaderboard ⏳ *chưa làm*

- Dùng **Spider** (tải sẵn trên mạng): đã kèm câu hỏi + SQL chuẩn + database + **script chấm chính thức** + leaderboard công khai.
- Quy trình: **tải Spider → chạy bộ sinh SQL của đồ án trên đó → chấm bằng script chính thức → so điểm với leaderboard**.
- Báo cáo: bảng "pipeline của tôi (gpt-4o / gpt-4o-mini) vs các hệ công bố" (trích dẫn nguồn + năm).

#### ⚠️ Vì sao "dùng API vẫn phải test" (giải thích để chống phản biện)

- Cái được đo **không phải** độ giỏi của OpenAI, mà là **toàn bộ pipeline của đồ án**:
  `prompt + cách mô tả schema + planner + guardrails + vòng repair` bọc quanh API.
  Cùng một model, prompt/schema khác nhau → kết quả khác nhau → con số là **"hệ của tôi đạt bao nhiêu %"**.
- **Không thể trích sẵn số của OpenAI** vì OpenAI không công bố con số Text-to-SQL nào; độ chính xác phụ thuộc cách dùng. Muốn có số phải **tự chạy hệ của mình rồi chấm**.
- **So với SOTA vẫn công bằng**: nhiều hệ top Spider/BIRD (DIN-SQL, DAIL-SQL…) **cũng dùng GPT-4 qua API**; khác biệt là phần prompt/pipeline — đúng thứ đồ án tự làm.
- **Phát biểu trung thực khi bảo vệ:** *"Em không huấn luyện mô hình sinh SQL. Đóng góp của em là hệ thống lakehouse + agent đọc-only có kiểm soát; LLM qua API là một thành phần. Benchmark Spider nhằm định lượng năng lực sinh SQL của pipeline em và đặt cạnh các hệ công bố."*
- **Đừng kỳ vọng đứng đầu**: nhiều hệ leaderboard được fine-tune riêng cho Spider; đồ án dùng LLM thương mại few-shot → thấp hơn là bình thường, mục tiêu là **định vị**.
- **Lưu ý phạm vi**: hệ đầy đủ bị khóa schema taxi + guardrails nên **không chạy nguyên trạng** trên Spider; chỉ **module sinh SQL** chạy được trên Spider. Guardrails/planner là đặc thù miền → ghi vào *threats to validity*.

### B2. Bộ test riêng 27 ca — pass/fail ✅ *đã có, cần đưa đầy đủ vào báo cáo*

- 27/27 PASS = 13 answer + 3 clarification + 11 blocked. Nguồn: [agent-evaluation-results.json](../agent-evaluation-results.json).
- Việc cần làm: lập **bảng pass/fail chi tiết từng ca** (case_id, bề mặt, kỳ vọng, kết quả) đưa vào phụ lục.

### B3. (Tùy chọn) Bộ taxi-nl2sql trong miền — ⏳ *cân nhắc, không bắt buộc*

- Tự xây ~60–100 cặp NL→SQL trên schema taxi để đo **hệ thống thật trong miền**.
- **Không phải yêu cầu của thầy** (thầy đã đủ với Spider + 27 ca). Chỉ làm nếu muốn báo cáo mạnh hơn.

---

## C. Các thông số cần đo & đưa đầy đủ vào chương kiểm thử

Đã có sẵn số liệu, cần trình bày đầy đủ trong chương Cài đặt & kiểm thử:

| Trục | Chỉ số | Trạng thái |
|---|---|---|
| Chất lượng dữ liệu | dbt tests 77 PASS / 2 WARN / 0 ERROR; lọc Bronze→Silver 1,53% | ✅ đã có trong `Chuong3-4.tex` |
| Hành vi agent | 27/27; unsafe_rejection / grounded / trace = 1.0 | ✅ đã có trong `Chuong3-4.tex` |
| Hiệu năng | mart p50 715ms vs star p50 1111ms; benchmark P01–P05 | ✅ đã có trong `Chuong3-4.tex` |
| **Sinh SQL (Spider)** | **EX vs leaderboard** | ❌ chưa — **làm mới (B1)** |

---

## D. Hạn chế cần nêu trung thực (threats to validity)

- Bộ 27 ca do tác giả tự thiết kế → selection bias.
- Không có nhãn vàng từ annotator độc lập (đánh giá ở mức grounded-on-rows).
- Đánh giá đơn lượt (single-turn).
- Cửa sổ dữ liệu hẹp (2024-H1, 6 tháng); chỉ Yellow + Green.
- Đo trên phần cứng cục bộ, trong Docker.
- Trên Spider chỉ đánh giá **module sinh SQL**, không phải hệ đầy đủ có guardrails.

---

## E. Thứ tự ưu tiên đề xuất (cập nhật theo việc CÒN LẠI)

> Đã xong: A1, A2, A4, A5, A6, A7 + mục C, D đã có trong `Chuong3-4.tex`.

1. **A8 — Viết Kết luận** + **A9 — bỏ comment link GitHub ở Phụ lục A** (sửa nhanh bằng text).
2. **A3 — Chèn 9 ảnh thật** vào các khung placeholder (cần ảnh chụp/sơ đồ).
3. **B1 — Benchmark Spider** (chạy thí nghiệm để có số EX vs leaderboard).
4. **B3 (tùy chọn)** — bộ taxi-nl2sql trong miền, nếu muốn báo cáo mạnh hơn.
