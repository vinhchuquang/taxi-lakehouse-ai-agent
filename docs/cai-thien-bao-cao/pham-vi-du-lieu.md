# Phạm vi dữ liệu — cách viết & bảo vệ (chống ấn tượng "dữ liệu bé")

Nội dung sẵn để ghép vào báo cáo (Chương 1 mục phạm vi và/hoặc Chương 4). Mục tiêu:
làm rõ dữ liệu **không nhỏ** bằng cách tách **phạm vi năng lực hệ thống** khỏi
**phạm vi đánh giá cố định**.

> Số liệu thật (truy vấn `fact_trips` ngày chốt báo cáo):
> - Tổng: **102.068.992** chuyến · Khoảng ngày pickup: **2023-12-01 → 2026-03-31** (~28 tháng).
> - Theo năm: 2023 = 3.397.904 · 2024 = 41.096.192 · 2025 = 46.463.163 · 2026 = 11.111.733.
> - Cửa sổ đánh giá **2024-H1**: **20.354.795** chuyến.

---

## 1. Nguyên tắc trình bày (ghi nhớ khi viết & khi nói)

- **KHÔNG mở đầu bằng "6 tháng"** (nghe nhỏ). **Mở đầu bằng khối lượng**: "20,35 triệu
  chuyến trong cửa sổ đánh giá; hơn 102 triệu chuyến trên toàn kho".
- Luôn để **bảng 2 cột**: *Toàn kho (năng lực)* vs *2024-H1 (đánh giá)*.
- Khung lại: cửa sổ 6 tháng là **lựa chọn về tính tái lập**, không phải giới hạn năng lực.

## 2. Bảng đề xuất chèn vào báo cáo

**Bảng x.y: Hai phạm vi dữ liệu của đồ án**

| Tiêu chí | Toàn kho (năng lực hệ thống) | 2024-H1 (phạm vi đánh giá) |
|---|---|---|
| Khoảng thời gian | 12/2023 – 03/2026 (~28 tháng) | 01–06/2024 (6 tháng) |
| Số chuyến (`fact_trips`) | 102.068.992 | 20.354.795 |
| Riêng năm 2024 | 41.096.192 | — |
| Mục đích | Chứng minh khả năng xử lý quy mô lớn, đa năm | Cố định để bảo đảm kết quả tái lập |

## 3. Đoạn văn cho mục Phạm vi (Chương 1) hoặc đầu Chương 4

> **Phạm vi dữ liệu.** Cần phân biệt hai phạm vi trong đồ án. Thứ nhất là *phạm vi
> năng lực của hệ thống*: pipeline đã thu thập và xử lý toàn bộ dữ liệu Yellow Taxi
> và Green Taxi do NYC TLC công bố trong khoảng từ 12/2023 đến 03/2026, tương ứng
> hơn 102 triệu chuyến đi hợp lệ ở bảng `fact_trips`, trong đó riêng năm 2024 đã có
> hơn 41 triệu chuyến. Thứ hai là *phạm vi đánh giá*: nhằm bảo đảm tính tái lập của
> các kết quả thực nghiệm, toàn bộ phần đo đạc (chất lượng dữ liệu, hiệu năng và đánh
> giá AI Agent) được cố định trên cửa sổ 2024-H1 (01/01/2024–30/06/2024), gồm
> 20,35 triệu chuyến. Việc đóng băng cửa sổ đánh giá là cần thiết vì kho dữ liệu tiếp
> tục được nạp định kỳ theo tháng; nếu lấy toàn bộ kho làm mốc, số liệu sẽ thay đổi
> sau mỗi lần chạy pipeline và không thể tái lập khi bảo vệ.

## 4. Đoạn văn cho mục Hạn chế (threats to validity)

> Phạm vi đánh giá được giới hạn ở cửa sổ 2024-H1 nhằm bảo đảm tính tái lập, và
> không phản ánh giới hạn năng lực xử lý của hệ thống: trên thực tế pipeline đã vận
> hành trên toàn kho hơn 102 triệu chuyến trải hơn hai năm. Hạn chế còn lại của việc
> cố định cửa sổ là chưa khảo sát đầy đủ hiệu ứng mùa vụ và biến động liên năm; có
> thể mở rộng bằng cách lặp lại quy trình đánh giá trên các cửa sổ thời gian khác mà
> không cần thay đổi kiến trúc.

## 5. Câu chốt khi bảo vệ (học thuộc)

> "Dữ liệu của em không nhỏ: riêng cửa sổ đánh giá 2024-H1 đã hơn 20 triệu chuyến,
> toàn kho hơn 100 triệu chuyến trải hơn hai năm. Em cố định cửa sổ đánh giá để kết
> quả tái lập được, chứ không phải vì thiếu dữ liệu."

## 6. Lưu ý nhất quán số liệu

- Báo cáo cũ (Bảng 3.8) ghi full ~98 triệu; nay là ~102 triệu do đã nạp thêm. Khi
  viết, ghi rõ **"tại thời điểm chốt báo cáo, kho chứa 102.068.992 chuyến"** để có
  mốc cố định, tránh bị hỏi vặn vì số đổi.
- Giữ **mọi bảng số liệu kèm 2 cột "Toàn kho / 2024-H1"** (như Bảng 3.8) — vừa minh
  bạch vừa thể hiện quy mô.
