# Chương 3 — Phân tích & thiết kế hệ thống

**Mục tiêu chương:** mô tả kiến trúc & thiết kế. KHÔNG lệnh chạy/cấu hình (để Chương 4).

**Tái dùng từ báo cáo cũ:** **gần như NGUYÊN Chương 2 cũ** ("Phân tích thiết kế hệ thống"
đã viết tốt). Chủ yếu **đánh số lại 2.x → 3.x** + thêm mục lập luận kiến trúc.

## Tài liệu cần đính kèm khi gửi AI
- **Toàn bộ Chương 2 báo cáo cũ** (`main (14).pdf`) ✅ — nguồn chính
- [../architecture.md](../architecture.md), [../thesis/architecture-diagrams.md](../thesis/architecture-diagrams.md) ✅
- [../modeling-decisions.md](../modeling-decisions.md), [../gold-star-schema.md](../gold-star-schema.md) ✅
- [../data-contracts.md](../data-contracts.md) ✅
- [../../contracts/semantic_catalog.yaml](../../contracts/semantic_catalog.yaml) ✅

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
- Đề xuất vị trí hình/bảng bằng chú thích "Hình 3.y: ..." / "Bảng 3.y: ...".
- Thuật ngữ nhất quán: Bronze/Silver/Gold, ELT, star schema, semantic catalog,
  guardrails, Text-to-SQL, agent.

# Ràng buộc
- KHÔNG thêm tính năng ngoài phạm vi (FHV/HVFHV, streaming, write-agent, cloud).
- KHÔNG bịa số liệu; giữ nguyên các bảng/sơ đồ thiết kế đã có.

# YÊU CẦU: viết "Chương 3 — Phân tích và thiết kế hệ thống"
Dựa trên Chương 2 của báo cáo cũ (đính kèm). Phần lớn GIỮ NGUYÊN nội dung, chỉ:
- Đánh số lại các mục thành 3.1–3.9.
- Thêm 1 mục cuối "3.10 Lập luận lựa chọn kiến trúc": vì sao chọn Lakehouse (không
  phải DW/Lake thuần), ELT (không ETL), star schema (không 3NF/bảng phẳng), Gold
  2 lớp (mart + fact), agent đọc-only, guardrails allow-list.

## Cấu trúc (đánh số 3.1–3.10)
3.1 Mục tiêu và nguyên tắc thiết kế kiến trúc.
3.2 Kiến trúc tổng thể của hệ thống (7 thành phần; hai nửa pipeline/tiêu thụ).
3.3 Thiết kế luồng dữ liệu ELT.
3.4 Thiết kế tầng Bronze / Silver / Gold.
3.5 Thiết kế mô hình chiều và bảng fact (star schema: fact_trips + 5 dimension).
3.6 Thiết kế lớp ngữ nghĩa (semantic catalog).
3.7 Thiết kế API truy vấn chỉ đọc (FastAPI; 3 endpoint).
3.8 Thiết kế AI Agent Text-to-SQL (state machine phi trạng thái).
3.9 Thiết kế hệ guardrails 3 tầng và nguyên tắc an toàn.
3.10 Lập luận lựa chọn kiến trúc (mục bổ sung mới).

## Ràng buộc riêng
- KHÔNG đưa lệnh chạy/cấu hình/lệnh Docker (để Chương 4).
- Giữ nguyên các bảng/sơ đồ thiết kế (star schema, vai trò thành phần, join paths).
```
