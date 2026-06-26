# Chương 1 — Phát biểu bài toán

**Mục tiêu chương:** đặt vấn đề, mục tiêu, phạm vi, các bên liên quan, đóng góp.
KHÔNG đi vào lý thuyết chi tiết (Chương 2) hay thiết kế (Chương 3).

**Tái dùng từ báo cáo cũ:** Chương 1 cũ (1.1 Tổng quan, 1.3 Phạm vi, 1.4 Khảo sát bên
liên quan, 1.6 Các bài toán quan tâm). **Bỏ** 1.2 (lý thuyết) và 1.7 (công nghệ) → chuyển Chương 2.

## Tài liệu cần đính kèm khi gửi AI
- Nội dung **Chương 1 báo cáo cũ** (`main (14).pdf`) ✅
- [../thesis/thesis-outline.md](../thesis/thesis-outline.md) — mục Chương 1 ✅
- [../../AGENTS.md](../../AGENTS.md) — phạm vi & "Do Not" ✅
- [../../README.md](../../README.md) — mô tả tổng quan ✅

---

## PROMPT (copy nguyên khối dưới đây)

```text
Bạn là trợ lý viết luận văn tốt nghiệp kỹ thuật bằng tiếng Việt học thuật.

# Bối cảnh đề tài
Đồ án xây dựng một Data Lakehouse cục bộ cho dữ liệu chuyến đi taxi NYC TLC
(Yellow + Green Taxi), tổ chức theo các tầng Bronze – Silver – Gold, kèm một
AI Agent Text-to-SQL CHỈ ĐỌC truy vấn trên tầng Gold qua một lớp ngữ nghĩa có
kiểm soát (semantic catalog) và hệ guardrails. Toàn bộ chạy local-first bằng
Docker Compose. Phạm vi dữ liệu cố định: 2024-01-01 đến 2024-06-30 (2024-H1).

# Cấu trúc báo cáo MỚI gồm 4 chương
Ch.1 Phát biểu bài toán · Ch.2 Cơ sở lý thuyết & công nghệ · Ch.3 Phân tích &
thiết kế · Ch.4 Cài đặt & kiểm thử. Tài liệu đính kèm có thể đánh số chương khác
— hãy BỎ QUA cách đánh số đó, chỉ lấy dữ kiện; báo cáo của tôi dùng đúng 4 chương.

# Quy tắc trình bày
- Văn phong học thuật, trang trọng, ngôi trung tính; KHÔNG dùng "tôi/chúng tôi/em".
- Viết đoạn văn liền mạch là chính; gạch đầu dòng chỉ cho danh sách.
- Mỗi mục mở đầu bằng 1–2 câu dẫn nối.
- Đề xuất vị trí hình/bảng bằng chú thích "Hình 1.y: ..." / "Bảng 1.y: ...".
- Thuật ngữ nhất quán: Bronze/Silver/Gold, ELT, star schema, semantic catalog,
  guardrails, Text-to-SQL, agent.

# Ràng buộc
- KHÔNG thêm tính năng ngoài phạm vi: FHV/HVFHV, streaming, agent ghi dữ liệu,
  multi-turn, cloud/production.
- KHÔNG bịa số liệu; cần minh họa thêm phải ghi rõ "ví dụ minh họa".

# YÊU CẦU: viết HOÀN CHỈNH "Chương 1 — Phát biểu bài toán"

## Cấu trúc (đánh số 1.1–1.7)
1.1 Bối cảnh và động lực (dữ liệu TLC công khai hàng trăm triệu chuyến/năm; xu
    hướng Lakehouse; nhu cầu phân tích bằng ngôn ngữ tự nhiên an toàn).
1.2 Vấn đề cần giải quyết (truy vấn dữ liệu lớn bằng NNTN mà vẫn kiểm soát an
    toàn, không lộ dữ liệu thô, không thao tác ghi).
1.3 Mục tiêu và câu hỏi nghiên cứu (4 mục tiêu: pipeline lặp lại được; star
    schema; agent đọc-only có guardrails; đánh giá định lượng).
1.4 Phạm vi và giới hạn (TRONG: Yellow+Green, Taxi Zone Lookup, 2024-H1,
    local-first, read-only. NGOÀI: FHV/HVFHV, streaming, write-agent, cloud).
1.5 Khảo sát các bên liên quan và nhu cầu (nhóm phân tích/nghiệp vụ, kỹ thuật
    dữ liệu, người dùng hỏi đáp).
1.6 Đóng góp chính của đồ án (lakehouse local-first end-to-end; star schema có
    kiểm chứng; agent đọc-only tự xây có trace; bộ đánh giá tái lập).
1.7 Cấu trúc báo cáo (tóm tắt 3 chương còn lại trong 1 đoạn).

## Nội dung nguồn
Dựa trên Chương 1 của báo cáo cũ (đính kèm) và AGENTS.md cho phạm vi/giới hạn.
Giữ nguyên các luận điểm, tổ chức lại theo 1.1–1.7 và loại bỏ phần lý thuyết &
công nghệ (đã chuyển sang Chương 2).

## Độ dài: 6–8 trang A4.
```
