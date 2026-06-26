# Cải thiện báo cáo — bộ tài liệu theo từng chương

Thư mục này gom mọi thứ để **sửa & viết lại báo cáo theo cấu trúc 4 chương mới**,
chia theo từng chương để làm tuần tự.

## Mục lục thư mục

| File | Nội dung |
|---|---|
| `00-README.md` | Tài liệu này: tổng quan + cách dùng + thứ tự |
| `00a-prompt-tai-cau-truc.md` | **Bước 0** — prompt tái cấu trúc tổng thể 3→4 chương |
| `01-chuong-1-phat-bieu-bai-toan.md` | Prompt + tài liệu cho **Chương 1** |
| `02-chuong-2-co-so-ly-thuyet-cong-nghe.md` | Prompt + tài liệu cho **Chương 2** |
| `03-chuong-3-phan-tich-thiet-ke.md` | Prompt + tài liệu cho **Chương 3** |
| `04-chuong-4-cai-dat-kiem-thu.md` | Prompt + tài liệu cho **Chương 4** |
| `pham-vi-du-lieu.md` | Đoạn văn + bảng sẵn về **phạm vi dữ liệu** (chống ấn tượng "dữ liệu bé") |
| [ke-hoach-sua-bao-cao-4-chuong.md](ke-hoach-sua-bao-cao-4-chuong.md) | Kế hoạch tổng thể tái cấu trúc 3→4 chương |
| [cai-thien-do-an.md](cai-thien-do-an.md) | Danh sách tổng các điểm cần cải thiện |
| [chuong3-sua-loi.md](chuong3-sua-loi.md) | Bản sửa lỗi chương cài đặt (áp dụng cho Chương 4 mới) |

## Cách dùng mỗi file chương
1. Mở file chương cần làm.
2. **Copy nguyên khối prompt** trong file đó (đã gồm sẵn phần bối cảnh chung).
3. Đính kèm: **nội dung báo cáo cũ** (`main (14).pdf`) **+** các file liệt kê ở đầu file chương.
4. Gửi cho AI. Có kết quả thì lưu lại và chuyển sang chương kế tiếp.

## Cấu trúc 4 chương mới
- **Chương 1 — Phát biểu bài toán** (← Ch.1 cũ, bỏ lý thuyết & công nghệ)
- **Chương 2 — Cơ sở lý thuyết & các thành phần công nghệ** (← gom 1.2 + 1.7 cũ + mở rộng)
- **Chương 3 — Phân tích & thiết kế** (← gần như nguyên Ch.2 cũ)
- **Chương 4 — Cài đặt & kiểm thử** (← Ch.3 cũ + mở rộng đánh giá + benchmark Spider)

## Thứ tự thực hiện đề xuất
0. **Bước 0 — Tái cấu trúc** (`00a-prompt-tai-cau-truc.md`): cho AI sắp xếp khung
   3→4 chương, ra mục lục mới + bản đồ nội dung cũ→mới. Làm TRƯỚC tiên.
1. **Chương 1** — gọn, cắt từ Ch.1 cũ → quen quy trình.
2. **Chương 3** — gần như nguyên Ch.2 cũ → nhanh, ít rủi ro.
3. **Chương 2** — lắp ghép lý thuyết + công nghệ.
4. **Chạy benchmark Spider** (xem [cai-thien-do-an.md](cai-thien-do-an.md) mục B1) → có số.
5. **Chương 4** — cần số Spider ở mục 4.10.2; các phần khác viết trước, chừa placeholder.

## Quy ước
- ✅ = tài liệu đã có trong repo · ❌ = phải làm mới trước khi viết.
- Mọi prompt đã nhúng sẵn phần "bối cảnh chung" + ràng buộc, **không cần** dán thêm gì.
