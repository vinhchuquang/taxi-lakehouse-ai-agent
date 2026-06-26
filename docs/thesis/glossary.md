# Bảng thuật ngữ Việt – Anh

Dùng để giữ thuật ngữ **nhất quán** trong toàn bộ báo cáo và slide. Khi gặp
một từ tiếng Anh phổ biến mà không có tiếng Việt tương đương rõ, giữ nguyên
tiếng Anh và in nghiêng.

> Quy ước:
> - **Giữ nguyên tiếng Anh (in nghiêng)** với các tên công nghệ và một số
>   khái niệm chuyên ngành đã ổn định toàn cầu (vd: *DuckDB*, *Airflow*,
>   *Bronze/Silver/Gold*, *Lakehouse*).
> - **Dịch sang tiếng Việt** với các khái niệm cơ bản về CSDL và phân tích
>   (vd: bảng sự kiện, bảng chiều, độ trễ).
> - Lần đầu xuất hiện trong báo cáo, viết: **tiếng Việt (tiếng Anh)**.
>   Các lần sau dùng tiếng Việt thuần.

---

## 1. Kiến trúc dữ liệu

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Data Lakehouse | Lakehouse / Hồ-kho dữ liệu | Giữ nguyên là tốt nhất; "hồ-kho dữ liệu" chỉ dùng khi giải thích lần đầu |
| Data Lake | Hồ dữ liệu | |
| Data Warehouse | Kho dữ liệu | |
| Bronze / Silver / Gold layer | Lớp Bronze / Silver / Gold | Giữ nguyên tên lớp |
| Medallion architecture | Kiến trúc medallion | |
| Object storage | Lưu trữ đối tượng | |
| Source of truth | Nguồn xác thực / nguồn gốc | |
| Ingestion | Tiếp nhận dữ liệu / ingestion | "Ingestion" thường dùng hơn |
| Pipeline | Luồng xử lý / pipeline | |
| Orchestration | Điều phối | |
| DAG (Directed Acyclic Graph) | Đồ thị có hướng không chu trình | Giữ "DAG" sau lần đầu |
| Backfill | Chạy bổ sung dữ liệu cũ / backfill | |
| Lookback | Lookback / cửa sổ rà soát lại | |
| Partition | Phân mảnh / partition | |
| Manifest | Manifest / bản kê | |
| Checksum | Tổng kiểm SHA-256 | |
| Idempotency | Tính khôn-trùng / idempotency | Giữ tiếng Anh là phổ biến |
| Atomic promote | Chuyển trạng thái nguyên tử | |

## 2. Mô hình hóa dữ liệu

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Dimensional modeling | Mô hình hóa đa chiều | |
| Star schema | Lược đồ hình sao | Giữ "star schema" sau lần đầu |
| Snowflake schema | Lược đồ bông tuyết | |
| Fact table | Bảng sự kiện | |
| Dimension table | Bảng chiều | |
| Measure / Metric | Độ đo / chỉ số | |
| Conformed dimension | Bảng chiều chuẩn hóa | |
| Slowly Changing Dimension (SCD) | Bảng chiều thay đổi chậm | Giữ "SCD Type 1/2" |
| Surrogate key | Khóa thay thế | |
| Natural key | Khóa tự nhiên | |
| Foreign key | Khóa ngoại | |
| Grain | Mức chi tiết / grain | |
| Aggregate mart | Mart tổng hợp | |
| Materialized view | View vật chất hóa | |
| Wide table | Bảng phẳng / wide table | |

## 3. Công cụ và stack

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Apache Airflow | Apache Airflow | Giữ nguyên |
| dbt (data build tool) | dbt | Giữ nguyên |
| DuckDB | DuckDB | Giữ nguyên |
| MinIO | MinIO | Giữ nguyên |
| FastAPI | FastAPI | Giữ nguyên |
| Streamlit | Streamlit | Giữ nguyên |
| Docker / Docker Compose | Docker / Docker Compose | Giữ nguyên |
| SQL | SQL | Giữ nguyên |
| Python | Python | Giữ nguyên |
| sqlglot | sqlglot | Giữ nguyên (tên thư viện) |
| OpenAI API | OpenAI API | Giữ nguyên |
| httpfs extension | Tiện ích httpfs | DuckDB extension đọc trực tiếp object storage |

## 4. AI agent và Text-to-SQL

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| AI agent | AI agent / tác tử AI | "AI agent" được dùng phổ biến hơn |
| Read-only agent | Agent đọc-only / agent chỉ đọc | |
| Agent orchestrator | Bộ điều phối agent | |
| State machine | Máy trạng thái | |
| Workflow | Luồng công việc / workflow | |
| Tool calling | Gọi công cụ / tool calling | |
| Large Language Model (LLM) | Mô hình ngôn ngữ lớn | Giữ "LLM" sau lần đầu |
| Prompt | Prompt / lời gợi | "Prompt" phổ biến hơn |
| Prompt engineering | Kỹ thuật prompt | |
| Prompt injection | Tiêm prompt / prompt injection | |
| Text-to-SQL | Sinh SQL từ ngôn ngữ tự nhiên | Giữ "Text-to-SQL" sau lần đầu |
| Natural language question | Câu hỏi ngôn ngữ tự nhiên | |
| Intent | Ý định | |
| Plan / planning | Kế hoạch / lập kế hoạch | |
| Self-check | Tự kiểm tra | |
| Hallucination | Ảo giác / hallucination | "Hallucination" dùng phổ biến |
| Grounding | Bám vào bằng chứng / grounding | |
| Deterministic answer | Câu trả lời xác định | Khác với câu trả lời do LLM tổng hợp |
| Answer synthesis | Tổng hợp câu trả lời | |
| Trace | Vết / trace | |
| `agent_steps` | Các bước agent | Trường JSON trong response |

## 5. Guardrails và an toàn

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Guardrail | Rào chắn / guardrail | Giữ "guardrail" sau lần đầu |
| Validation | Kiểm tra / kiểm chứng | |
| Allow-list | Danh sách cho phép | |
| Deny-list / block-list | Danh sách cấm | |
| Read-only mode | Chế độ chỉ đọc | |
| DDL (Data Definition Language) | Lệnh định nghĩa dữ liệu | CREATE/DROP/ALTER |
| DML (Data Manipulation Language) | Lệnh thao tác dữ liệu | INSERT/UPDATE/DELETE |
| Wildcard | Ký tự đại diện | `SELECT *` |
| AST (Abstract Syntax Tree) | Cây cú pháp trừu tượng | |
| Cartesian join | JOIN tích Descartes | |
| Allowed joins | Các JOIN được phép | |
| Schema linking | Liên kết schema | |
| Semantic catalog | Danh mục ngữ nghĩa | |
| Audit log | Nhật ký kiểm tra / audit log | |

## 6. Chất lượng dữ liệu và kiểm thử

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Data quality | Chất lượng dữ liệu | |
| dbt test | Kiểm thử dbt | |
| Unit test | Kiểm thử đơn vị | |
| Smoke test | Smoke test / kiểm thử nhanh | |
| Regression test | Kiểm thử hồi quy | |
| Pass / Warn / Error / Skip | Pass / Warn / Error / Skip | Giữ nguyên trong kết quả dbt |
| Anomaly | Bất thường | |
| Validity filter | Bộ lọc hợp lệ | |
| Quality gate | Cổng chất lượng | |
| Reproducibility | Tính tái lập | |
| Benchmark | Phép đo chuẩn / benchmark | |
| Latency | Độ trễ | |
| Throughput | Thông lượng | |
| p50 / p95 / p99 | Phân vị 50 / 95 / 99 | Hoặc giữ "p50/p95/p99" |

## 7. Triển khai và vận hành

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Local-first | Local-first / ưu tiên cục bộ | |
| Container | Container | Giữ nguyên |
| Image | Image | Giữ nguyên trong bối cảnh Docker |
| Volume | Volume | Giữ nguyên trong bối cảnh Docker |
| Service | Dịch vụ / service | |
| Endpoint | Endpoint / điểm cuối | |
| Healthcheck | Healthcheck / kiểm tra sống | |
| Continuous Integration (CI) | Tích hợp liên tục | |
| Continuous Delivery (CD) | Phân phối liên tục | |
| Deployment | Triển khai | |
| Observability | Khả năng quan sát | |
| Monitoring | Giám sát | |
| Alerting | Cảnh báo | |
| SLO / SLA | Mục tiêu / cam kết mức dịch vụ | Giữ "SLO/SLA" |
| Rate limiting | Giới hạn tần suất | |

## 8. Đánh giá học thuật

| Tiếng Anh | Tiếng Việt | Ghi chú |
|---|---|---|
| Threats to validity | Mối đe dọa tính hợp lệ | |
| Selection bias | Sai số chọn mẫu / selection bias | |
| Ground truth | Nhãn vàng / ground truth | |
| Baseline | Mốc so sánh / baseline | |
| Single-turn / multi-turn | Đơn lượt / nhiều lượt | |
| Out of scope | Ngoài phạm vi | |
| Future work | Hướng phát triển | |
| Contribution | Đóng góp | |
| Limitation | Hạn chế | |

---

## Thuật ngữ tên riêng giữ nguyên

- **NYC TLC (New York City Taxi and Limousine Commission)** — Cơ quan quản lý
  Taxi và xe limousine thành phố New York.
- **Yellow Taxi**, **Green Taxi** — Hai loại dịch vụ taxi truyền thống ở NYC.
- **FHV (For-Hire Vehicle)**, **HVFHV (High-Volume FHV)** — Xe dịch vụ thuê,
  bao gồm Uber/Lyft. *Ngoài phạm vi đồ án.*
- **Kimball** — Ralph Kimball, tên người sáng lập trường phái dimensional
  modeling.

## Viết tắt thường dùng

| Viết tắt | Đầy đủ |
|---|---|
| BI | Business Intelligence |
| API | Application Programming Interface |
| AST | Abstract Syntax Tree |
| CSDL | Cơ sở dữ liệu |
| DAG | Directed Acyclic Graph |
| DDL / DML | Data Definition / Manipulation Language |
| ETL / ELT | Extract-Transform-Load / Extract-Load-Transform |
| KPI | Key Performance Indicator |
| LLM | Large Language Model |
| OIDC | OpenID Connect |
| OLAP | Online Analytical Processing |
| OLTP | Online Transaction Processing |
| ORM | Object-Relational Mapping |
| SCD | Slowly Changing Dimension |
| SLO / SLA | Service Level Objective / Agreement |
| TLC | (NYC) Taxi & Limousine Commission |
| YAML | YAML Ain't Markup Language |

---

## Hướng dẫn dùng glossary

1. Khi viết báo cáo, mỗi lần lần **đầu** dùng một thuật ngữ tiếng Anh, viết
   theo dạng: *"Lakehouse (Hồ-kho dữ liệu)"* hoặc *"Lakehouse"* nếu giữ
   nguyên.
2. Các lần sau dùng đúng một dạng — đừng đổi qua lại.
3. Trong tóm tắt và keywords, dùng tiếng Anh nguyên dạng cho thuật ngữ
   chuyên ngành (vd: *Lakehouse*, *Dimensional modeling*, *Text-to-SQL*,
   *Guardrails*).
4. Nếu giảng viên hướng dẫn yêu cầu thuần Việt, ưu tiên cột "Tiếng Việt" và
   chú thích tiếng Anh trong dấu ngoặc.
