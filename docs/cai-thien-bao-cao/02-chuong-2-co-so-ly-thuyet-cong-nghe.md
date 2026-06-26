# Chương 2 — Cơ sở lý thuyết & các thành phần công nghệ

**Mục tiêu chương:** nền lý thuyết + vai trò/lý thuyết của từng công nghệ. Đây là
chương lắp ghép nhiều nguồn (mới nhiều sau Chương 4).

**Tái dùng từ báo cáo cũ:** mục 1.2 (cơ sở lý thuyết) + 1.7 (công nghệ) của Chương 1 cũ.

## Tài liệu cần đính kèm khi gửi AI
- [../thesis/related-work.md](../thesis/related-work.md) ✅
- [../thesis/glossary.md](../thesis/glossary.md) ✅
- Mục **1.2 và 1.7 báo cáo cũ** (`main (14).pdf`) ✅
- [../modeling-decisions.md](../modeling-decisions.md) — lý thuyết star schema ✅
- [../architecture.md](../architecture.md) — vai trò từng công nghệ ✅

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
- Đề xuất vị trí hình/bảng bằng chú thích "Hình 2.y: ..." / "Bảng 2.y: ...".
- Thuật ngữ nhất quán: Bronze/Silver/Gold, ELT, star schema, semantic catalog,
  guardrails, Text-to-SQL, agent.

# Ràng buộc
- KHÔNG thêm tính năng ngoài phạm vi: FHV/HVFHV, streaming, agent ghi dữ liệu,
  multi-turn, cloud/production.
- KHÔNG bịa số liệu; cần minh họa thêm phải ghi rõ "ví dụ minh họa".

# YÊU CẦU: viết HOÀN CHỈNH "Chương 2 — Cơ sở lý thuyết và các thành phần công nghệ"

## Cấu trúc (đánh số 2.1–2.7)
2.1 Kiến trúc Lakehouse và mô hình Medallion (Bronze/Silver/Gold); so sánh với
    Data Warehouse và Data Lake thuần.
2.2 Mô hình hóa chiều theo Kimball: star schema, fact, dimension, conformed/
    role-playing dimension.
2.3 Mô hình ELT so với ETL truyền thống; lý do phù hợp dữ liệu phát hành theo tháng.
2.4 Text-to-SQL và AI agent: khái niệm; luồng intent→plan→sinh SQL→thực thi→
    self-check; các benchmark chuẩn (Spider, BIRD) và cách đo Execution Accuracy
    — làm nền cho phần đánh giá ở Chương 4.
2.5 An toàn truy vấn: guardrails, phân tích cú pháp AST, so sánh allow-list và
    deny-list; rủi ro Text-to-SQL (injection, hallucination, lạm dụng schema).
2.6 Các thành phần công nghệ dùng trong dự án (vai trò + lý thuyết ngắn cho mỗi
    cái): Apache Airflow (điều phối), dbt (mô hình hóa & test), DuckDB (engine
    OLAP cục bộ), MinIO (object storage S3-compatible), FastAPI (API), Streamlit
    (giao diện), sqlglot (parse/validate SQL), OpenAI API (sinh SQL).
2.7 Các nghiên cứu/giải pháp liên quan và khoảng trống đồ án giải quyết (đa số
    mẫu Text-to-SQL thiếu guardrails đủ mạnh; nhiều khung agent giấu workflow nên
    khó kiểm chứng — đồ án tự xây để trace được).

## Yêu cầu riêng
- Mỗi công nghệ ở 2.6 viết 1 đoạn: nó là gì + vì sao phù hợp vai trò trong đồ án
  (KHÔNG đưa lệnh cài đặt — để Chương 4).
- 2.4 và 2.5 phải đặt nền khái niệm cho Chương 4 (Spider, Execution Accuracy,
  3 tầng guardrails).
- Có trích dẫn tham khảo cho mỗi khái niệm/công nghệ, đánh dấu [n] để tôi điền danh mục.

## Độ dài: 8–12 trang A4.
```
