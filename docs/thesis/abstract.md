# Tóm tắt / Abstract

Mẫu tóm tắt **tiếng Việt** và **tiếng Anh** cho báo cáo tốt nghiệp. Mỗi tóm
tắt khoảng 200–280 từ — phù hợp với phần lớn template trường ở Việt Nam.

> Quy ước:
> - `[ ]` = nội dung cần điền cụ thể.
> - Số liệu lấy từ snapshot Phase 37; cập nhật nếu chạy lại đánh giá.
> - Sau khi điền xong, kiểm tra với cô/thầy hướng dẫn xem có cần điều chỉnh
>   số từ hay cấu trúc theo template trường không.

---

## A. Phiên bản tiếng Việt — DÀI (~280 từ, dùng cho báo cáo)

### TÓM TẮT

Đồ án xây dựng một nền tảng dữ liệu **Lakehouse** local-first cho dữ liệu
chuyến đi taxi của Cơ quan Quản lý Taxi và Xe Limousine thành phố New York
(NYC TLC), kèm theo một **AI agent đọc-only** truy vấn lớp dữ liệu phục vụ
bằng ngôn ngữ tự nhiên.

Hệ thống tổ chức dữ liệu thành ba lớp **Bronze → Silver → Gold** theo mô
hình *medallion*. Lớp Gold được mô hình hóa theo **star schema Kimball** gồm
một bảng sự kiện `fact_trips`, năm bảng chiều, và hai bảng tổng hợp
(*aggregate mart*) làm đường truy vấn nhanh. Pipeline được điều phối bằng
Apache Airflow, các phép biến đổi được hiện thực bằng dbt, dữ liệu thô
được lưu trên MinIO làm *object storage*, và DuckDB đóng vai trò engine
truy vấn cục bộ.

AI agent được thiết kế tường minh dưới dạng máy trạng thái gồm bảy bước:
phân tích ý định, lập kế hoạch, sinh SQL, kiểm guardrails, thực thi, tự
kiểm tra và trả lời. Ba tầng **guardrails** (cột, bảng, JOIN) sử dụng AST
parsing qua thư viện `sqlglot` đảm bảo agent chỉ truy cập các đối tượng đã
khai báo trong *semantic catalog*, không thực hiện DDL/DML, không truy
xuất lớp Bronze/Silver và không sinh JOIN trái phép.

Đồ án được đánh giá trên ba trục: chất lượng dữ liệu (77/2/0 dbt tests),
độ chính xác và an toàn của agent (27/27 trường hợp đạt yêu cầu trên bộ
kiểm thử hồi quy), và hiệu năng (độ trễ p95 dưới 3 giây cho truy vấn star
schema). Toàn bộ hệ thống có thể tái lập bằng Docker Compose trên một máy
cá nhân với dataset cố định nửa đầu năm 2024 (`2024-H1`).

**Từ khóa:** Lakehouse, Mô hình hóa đa chiều, Kimball, Text-to-SQL,
AI Agent, Guardrails, dbt, DuckDB, Airflow, NYC TLC.

---

## B. Phiên bản tiếng Việt — NGẮN (~150 từ, dùng cho mục lục/giới thiệu nhanh)

Đồ án xây dựng một nền tảng **Lakehouse** local-first cho dữ liệu taxi NYC
TLC, kèm AI agent đọc-only truy vấn dữ liệu bằng ngôn ngữ tự nhiên. Dữ liệu
được tổ chức theo ba lớp Bronze → Silver → Gold; lớp Gold dùng star schema
Kimball với một fact và năm dimension. Hệ thống dùng Airflow, dbt, MinIO,
DuckDB và FastAPI, đóng gói trong Docker Compose. AI agent thực thi theo
máy trạng thái bảy bước với ba tầng guardrails (cột, bảng, JOIN) dựa trên
AST parsing. Đánh giá đạt 77/2/0 dbt tests, 27/27 trường hợp agent qua bộ
kiểm thử hồi quy với tỉ lệ chặn truy vấn nguy hiểm 100%, và độ trễ p95
dưới 3 giây.

**Từ khóa:** Lakehouse, Star Schema, Text-to-SQL, AI Agent, Guardrails.

---

## C. Phiên bản tiếng Anh — DÀI (~280 từ)

### ABSTRACT

This thesis presents a local-first **Lakehouse** platform built on the
publicly available trip records of the New York City Taxi and Limousine
Commission (NYC TLC), together with a **read-only AI query agent** that
serves analytical questions in natural language.

Data is organised into three layers — **Bronze, Silver and Gold** — following
the medallion architecture. The Gold layer is modelled as a Kimball
**star schema** with one fact table (`fact_trips`), five dimensions, and
two **aggregate marts** that serve as a fast path for common dashboard and
agent queries. The pipeline is orchestrated by Apache Airflow, transformations
are implemented with dbt, raw data resides on MinIO as the **object-storage
source of truth**, and DuckDB acts as the in-process analytical engine.

The AI agent is implemented as an explicit seven-state workflow: intent
analysis, planning, SQL generation, guardrail validation, execution,
self-checking, and answer synthesis. Three layers of **guardrails** —
column, table, and join — based on AST parsing via `sqlglot` ensure that
the agent only touches objects declared in a **semantic catalog**, never
issues DDL/DML, never reaches into Bronze or Silver, and never produces
unapproved joins.

The system is evaluated along three axes: **data quality** (77 dbt tests
passing, 2 documented anomaly warnings, 0 errors), **agent correctness and
safety** (27 of 27 regression cases passed, 100% unsafe-rejection rate,
100% grounded-answer rate), and **performance** (p95 latency under three
seconds for star-schema queries). The entire stack is reproducible via
Docker Compose on a single workstation against a frozen first-half-2024
dataset.

**Keywords:** Lakehouse, Dimensional Modeling, Kimball Star Schema,
Text-to-SQL, AI Agent, SQL Guardrails, dbt, DuckDB, Airflow, NYC TLC.

---

## D. Phiên bản tiếng Anh — NGẮN (~150 từ)

This thesis presents a local-first Lakehouse platform for NYC TLC taxi
trip data with a read-only AI query agent. Data is organised into Bronze,
Silver and Gold layers following the medallion pattern; the Gold layer
uses a Kimball star schema with one fact and five dimensions. The platform
is built on Airflow, dbt, MinIO, DuckDB and FastAPI, packaged in Docker
Compose. The agent runs as a seven-state workflow with three layers of
guardrails — column, table and join — implemented via AST parsing. The
evaluation reports 77/2/0 dbt tests, 27 of 27 regression cases passing
with a 100% unsafe-rejection rate, and p95 latency under three seconds.

**Keywords:** Lakehouse, Star Schema, Text-to-SQL, AI Agent, Guardrails.

---

## E. Từ khóa đầy đủ (cho mục Keywords / Index Terms)

### Tiếng Việt
Lakehouse, Mô hình hóa đa chiều, Star schema Kimball, Bảng sự kiện và bảng
chiều, Aggregate mart, Sinh SQL từ ngôn ngữ tự nhiên (Text-to-SQL), AI agent
đọc-only, Guardrails, AST parsing, sqlglot, dbt, DuckDB, MinIO, Apache
Airflow, FastAPI, NYC TLC, Yellow Taxi, Green Taxi, Docker Compose,
Local-first, Đánh giá hồi quy.

### Tiếng Anh
Lakehouse, Dimensional Modeling, Kimball Star Schema, Fact and Dimension
Tables, Aggregate Mart, Text-to-SQL, Read-Only AI Agent, SQL Guardrails,
AST Parsing, sqlglot, dbt, DuckDB, MinIO, Apache Airflow, FastAPI, NYC TLC,
Yellow Taxi, Green Taxi, Docker Compose, Local-First, Regression Evaluation.

---

## F. Lời cảm ơn (mẫu)

«Mẫu — điều chỉnh tên người và cụm từ theo phong cách trường»

> Em xin gửi lời cảm ơn chân thành đến thầy/cô **[TÊN GVHD]** — Khoa
> **[KHOA]**, Trường **[TRƯỜNG]** — đã hướng dẫn em tận tình trong suốt quá
> trình thực hiện đồ án tốt nghiệp này. Sự góp ý cụ thể và đòi hỏi chặt chẽ
> của thầy/cô đã giúp em định hướng phạm vi rõ ràng và hoàn thiện sản phẩm
> ở mức có thể bảo vệ.
>
> Em cũng cảm ơn các thầy cô trong Khoa **[KHOA]** đã cung cấp nền tảng kiến
> thức về cơ sở dữ liệu, hệ thống phân tán và lập trình; cảm ơn các bạn cùng
> khóa đã trao đổi và đóng góp ý kiến trong quá trình em xây dựng hệ thống.
>
> Cuối cùng, em xin cảm ơn gia đình đã ủng hộ em trong suốt quá trình học
> tập và thực hiện đồ án.
>
> **[Thành phố]**, ngày **[XX]** tháng **[XX]** năm **[XXXX]**
>
> Sinh viên thực hiện
>
> **[HỌ VÀ TÊN]**

---

## G. Cam đoan (mẫu — nếu trường yêu cầu)

> Em xin cam đoan rằng đồ án tốt nghiệp với đề tài **"[TÊN ĐỀ TÀI]"** là
> công trình nghiên cứu của riêng em dưới sự hướng dẫn của thầy/cô
> **[TÊN GVHD]**. Các kết quả nêu trong đồ án là trung thực, các số liệu và
> bảng biểu được trích dẫn rõ nguồn gốc. Toàn bộ mã nguồn được lưu trong
> repository tại đường dẫn **[URL nếu có]** và có thể tái lập bằng các
> bước hướng dẫn trong tài liệu vận hành đi kèm.
>
> **[Thành phố]**, ngày **[XX]** tháng **[XX]** năm **[XXXX]**
>
> Sinh viên thực hiện
>
> **[HỌ VÀ TÊN]**

---

## Hướng dẫn dùng file

1. Chọn **một** bản tóm tắt tiếng Việt + **một** bản tiếng Anh. Đa số
   trường yêu cầu phiên bản dài (~250 từ) cho cả hai.
2. Điền `[ ]` rồi đối chiếu lại với:
   - [thesis-outline.md](thesis-outline.md) — Chương 1.4 (Đóng góp chính)
     để đảm bảo từ ngữ thống nhất.
   - [evaluation-methodology.md](evaluation-methodology.md) §4 để đảm bảo
     số liệu khớp.
3. Dùng [glossary.md](glossary.md) để tra thuật ngữ song ngữ — đặc biệt
   khi viết phiên bản tiếng Anh.
4. Khi đếm từ, có thể dùng công cụ Word "Word Count" hoặc lệnh
   `wc -w abstract.txt` (Linux/Mac) — đa số trường yêu cầu 200–300 từ.
