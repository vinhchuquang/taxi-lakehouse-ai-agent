# Bước 0 — Prompt tái cấu trúc tổng thể (3 chương → 4 chương)

**Mục tiêu:** trước khi viết chi tiết từng chương, cho AI **sắp xếp lại khung** báo cáo cũ
(3 chương) sang khung mới (4 chương): tạo mục lục mới + bản đồ chuyển nội dung cũ→mới +
chỉ ra phần thiếu cần viết. **Chưa viết chi tiết** — đó là việc của các Bước 1–4 (file 01–04).

## Tài liệu cần đính kèm khi gửi AI
- **Toàn bộ báo cáo cũ** (`main (14).pdf`) — cả 3 chương ✅
- [ke-hoach-sua-bao-cao-4-chuong.md](ke-hoach-sua-bao-cao-4-chuong.md) — bản đồ di chuyển nội dung ✅

---

## PROMPT (copy nguyên khối dưới đây)

```text
Bạn là trợ lý biên tập luận văn tốt nghiệp kỹ thuật bằng tiếng Việt học thuật.

# Bối cảnh đề tài
Đồ án xây dựng một Data Lakehouse cục bộ cho dữ liệu chuyến đi taxi NYC TLC
(Yellow + Green Taxi), tổ chức theo các tầng Bronze – Silver – Gold, kèm một
AI Agent Text-to-SQL CHỈ ĐỌC truy vấn trên tầng Gold qua một lớp ngữ nghĩa có
kiểm soát (semantic catalog) và hệ guardrails. Toàn bộ chạy local-first bằng
Docker Compose. Phạm vi dữ liệu cố định: 2024-01-01 đến 2024-06-30 (2024-H1).

# Hiện trạng
Báo cáo cũ (đính kèm) đang có 3 chương:
- Chương 1: Khảo sát và mô tả hệ thống ứng dụng.
- Chương 2: Phân tích thiết kế hệ thống.
- Chương 3: Cài đặt hệ thống.

# Yêu cầu mới của giảng viên: tách thành 4 chương
- Chương 1: Phát biểu bài toán (xoay quanh bài toán: bối cảnh, vấn đề, mục tiêu,
  phạm vi, các bên liên quan, đóng góp).
- Chương 2: Cơ sở lý thuyết và các thành phần công nghệ dùng trong dự án.
- Chương 3: Phân tích và thiết kế hệ thống.
- Chương 4: Cài đặt và kiểm thử (gồm kịch bản kiểm thử và đánh giá định lượng đầy đủ).

# NHIỆM VỤ CỦA BẠN TRONG BƯỚC NÀY
KHÔNG viết lại nội dung chi tiết. Chỉ làm phần TÁI CẤU TRÚC:

1. Đề xuất MỤC LỤC chi tiết của 4 chương mới (tới mức tiểu mục x.y), nhất quán
   với khung trên.

2. Lập BẢNG ÁNH XẠ NỘI DUNG: mỗi mục trong báo cáo cũ (1.1, 1.2, …, 3.x) đi về
   mục nào trong cấu trúc mới, kèm hành động: GIỮ NGUYÊN / CHUYỂN / GỘP / VIẾT LẠI / BỎ.

3. Liệt kê các phần CÒN THIẾU phải viết mới (chưa có trong báo cáo cũ), đặc biệt:
   phần đánh giá định lượng mở rộng ở Chương 4 (bộ test riêng pass/fail + benchmark
   sinh SQL trên bộ dữ liệu công khai so với leaderboard).

4. Gợi ý các ĐOẠN CHUYỂN TIẾP cần thêm ở đầu/cuối mỗi chương để mạch văn liền lạc
   sau khi sắp xếp lại.

# Quy tắc áp dụng khi tái cấu trúc
- Tách phần "cơ sở lý thuyết" (mục 1.2 cũ) và "công nghệ sử dụng" (mục 1.7 cũ) ra
  KHỎI Chương 1, dồn sang Chương 2 mới.
- Chương 1 mới chỉ giữ phần phát biểu bài toán: tổng quan, vấn đề, mục tiêu, phạm
  vi, khảo sát bên liên quan, đóng góp.
- Chương 2 cũ (Phân tích thiết kế) chuyển gần như NGUYÊN sang Chương 3 mới, chỉ
  đánh số lại; bổ sung 1 mục "lập luận lựa chọn kiến trúc".
- Chương 3 cũ (Cài đặt) chuyển sang Chương 4 mới và MỞ RỘNG phần kiểm thử/đánh giá.
- Không làm mất luận điểm nào của báo cáo cũ; nếu một mục bị tách đôi, ghi rõ tách
  phần nào đi đâu.

# Ràng buộc
- Văn phong học thuật, ngôi trung tính; KHÔNG dùng "tôi/chúng tôi/em".
- KHÔNG bịa nội dung mới ngoài việc sắp xếp; phần thiếu chỉ LIỆT KÊ tiêu đề, chưa viết.
- Giữ thuật ngữ nhất quán: Bronze/Silver/Gold, ELT, star schema, semantic catalog,
  guardrails, Text-to-SQL, agent.

# Định dạng đầu ra
Trả về theo đúng 4 phần: (1) Mục lục mới; (2) Bảng ánh xạ cũ→mới; (3) Danh sách
phần thiếu; (4) Gợi ý đoạn chuyển tiếp.
```

---

## Sau bước này
Có mục lục + bản đồ nội dung rồi, chuyển sang viết chi tiết theo thứ tự:
**01 (Ch.1) → 03 (Ch.3) → 02 (Ch.2) → chạy Spider → 04 (Ch.4)**.
