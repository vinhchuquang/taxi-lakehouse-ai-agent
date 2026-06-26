# Kế hoạch sửa báo cáo: 3 chương → 4 chương

> Theo góp ý của GVHD. Tài liệu này là **kế hoạch viết lại**, không phải nội dung
> báo cáo. Mọi số liệu dẫn ở đây lấy từ repo (đã kiểm chứng cho cửa sổ 2024-H1).

## 0. Tóm tắt góp ý của thầy

1. Tách báo cáo thành **4 chương**:
   - **Ch.1 — Phát biểu bài toán** (xoay quanh bài toán: bối cảnh, vấn đề, phạm vi).
   - **Ch.2 — Cơ sở lý thuyết & các thành phần/công nghệ** dùng trong dự án.
   - **Ch.3 — Phân tích & thiết kế hệ thống.**
   - **Ch.4 — Cài đặt & kiểm thử**: kịch bản kiểm thử + đo **đầy đủ thông số** chứng minh hệ thống tốt.
2. Phần **Agent** phải có **2 loại đánh giá**:
   - (A) Đo **tỷ lệ sinh SQL đúng** trên **một bộ dataset có nhãn**, **so sánh với các mô hình tốt nhất hiện tại**.
   - (B) Trên **bộ test riêng** của tác giả → thống kê **pass/fail**.

---

## 1. Cấu trúc 4 chương mới (mục lục đề xuất)

### Chương 1 — Phát biểu bài toán
- 1.1 Bối cảnh & động lực (chuyển đổi số, dữ liệu TLC, xu hướng Lakehouse + AI agent)
- 1.2 Vấn đề cần giải quyết (truy vấn dữ liệu lớn bằng NNTN an toàn, có kiểm soát)
- 1.3 Mục tiêu & câu hỏi nghiên cứu
- 1.4 Phạm vi & giới hạn (Yellow+Green, 2024-H1, local-first, read-only)
- 1.5 Khảo sát các bên liên quan & nhu cầu
- 1.6 Đóng góp chính của đồ án
- 1.7 Cấu trúc báo cáo

### Chương 2 — Cơ sở lý thuyết & các thành phần công nghệ
- 2.1 Kiến trúc Lakehouse & mô hình Medallion (Bronze/Silver/Gold)
- 2.2 Mô hình hóa chiều — Kimball star schema
- 2.3 Mô hình ELT vs ETL
- 2.4 Text-to-SQL, LLM agent & các benchmark (Spider, BIRD) — *nền cho Ch.4*
- 2.5 An toàn truy vấn: guardrails, AST parsing, allow-list vs deny-list
- 2.6 Các thành phần công nghệ dùng trong dự án (vai trò + lý thuyết):
  Airflow, dbt, DuckDB, MinIO, FastAPI, Streamlit, sqlglot, OpenAI API
- 2.7 Các nghiên cứu/giải pháp liên quan & khoảng trống đồ án giải quyết

### Chương 3 — Phân tích & thiết kế hệ thống
- 3.1 Mục tiêu & nguyên tắc thiết kế kiến trúc
- 3.2 Kiến trúc tổng thể (7 thành phần, 2 nửa: pipeline / tiêu thụ)
- 3.3 Thiết kế luồng dữ liệu ELT
- 3.4 Thiết kế tầng Bronze / Silver / Gold
- 3.5 Thiết kế mô hình chiều & bảng fact (star schema)
- 3.6 Thiết kế lớp ngữ nghĩa (semantic catalog)
- 3.7 Thiết kế API truy vấn chỉ đọc
- 3.8 Thiết kế AI Agent Text-to-SQL (state machine)
- 3.9 Thiết kế hệ guardrails 3 tầng & nguyên tắc an toàn

### Chương 4 — Cài đặt & kiểm thử
- 4.1 Môi trường & công nghệ triển khai (Docker Compose 7 service)
- 4.2 Cài đặt pipeline ingestion (Airflow)
- 4.3 Cài đặt mô hình hóa dữ liệu (dbt, 12 model)
- 4.4 Cài đặt lớp ngữ nghĩa & API (FastAPI)
- 4.5 Cài đặt AI Agent & guardrails
- 4.6 Cài đặt giao diện Streamlit
- **4.7 Phương pháp kiểm thử & đánh giá** (3 trục + bộ benchmark agent)
- **4.8 Kết quả chất lượng dữ liệu** (dbt tests, lọc Bronze→Silver)
- **4.9 Kết quả hiệu năng** (benchmark P01–P05, latency theo bề mặt)
- **4.10 Đánh giá AI Agent**
  - 4.10.1 Bộ test riêng — pass/fail (27 ca)
  - 4.10.2 **Độ chính xác sinh SQL trên bộ dataset có nhãn + so sánh SOTA** *(MỚI)*
- 4.11 Hạn chế & threats to validity
- 4.12 Kết luận chương
- (sau Ch.4) Kết luận chung & hướng phát triển

---

## 2. Bản đồ di chuyển nội dung (báo cáo cũ 3 chương → mới 4 chương)

| Nội dung hiện có (main 14) | Vị trí mới | Hành động |
|---|---|---|
| Ch.1.1 Tổng quan bài toán | Ch.1.1–1.2 | Giữ, gọt theo hướng "phát biểu bài toán" |
| Ch.1.2 Cơ sở lý thuyết | **Ch.2.1–2.5** | **Chuyển** sang chương lý thuyết, mở rộng |
| Ch.1.3 Phạm vi & dữ liệu | Ch.1.4 | Giữ |
| Ch.1.4 Khảo sát bên liên quan | Ch.1.5 | Giữ |
| Ch.1.5 Quy trình hệ thống | Ch.1.5 / Ch.3.2 | Tách: nhu cầu→Ch.1, luồng kỹ thuật→Ch.3 |
| Ch.1.6 Các bài toán quan tâm | Ch.1.2–1.3 | Gộp vào phát biểu bài toán |
| Ch.1.7 Công nghệ sử dụng | **Ch.2.6** | **Chuyển** sang chương lý thuyết/thành phần |
| Ch.2 (toàn bộ thiết kế) | **Ch.3** | **Chuyển nguyên**, đánh số lại 3.x |
| Ch.3.1–3.6 (cài đặt) | **Ch.4.1–4.6** | Chuyển + áp dụng bản sửa lỗi `chuong3-sua-loi.md` |
| Ch.3.7 (kết quả/kiểm thử) | **Ch.4.7–4.11** | **Tách & mở rộng mạnh** (thêm benchmark agent) |
| Ch.3.8 Kết luận chương | Ch.4.12 | Giữ |

> Lưu ý: **bản sửa lỗi đã làm** ([chuong3-sua-loi.md](chuong3-sua-loi.md)) vẫn áp dụng
> cho nội dung này khi nó chuyển sang Ch.4 (lỗi lặp từ, `agent.py`, lệnh `--build`,
> đường dẫn audit, v.v.).

---

## 3. TRỌNG TÂM MỚI — Kế hoạch đánh giá AI Agent (mục 4.10)

Đây là phần tốn công nhất và là yêu cầu chính của thầy.

### 3.1 Hai loại đánh giá (phân biệt rõ)

| | (A) Độ chính xác sinh SQL trên benchmark công khai | (B) Bộ test hành vi riêng |
|---|---|---|
| Mục tiêu | Tỷ lệ sinh SQL đúng **trên bộ dữ liệu công khai đã có leaderboard**, so với người khác | Agent **hành xử đúng** không (answer/clarify/block) |
| Dữ liệu | **Spider** (hoặc BIRD) — bộ chuẩn ngành, có điểm công bố sẵn | 27 ca hiện có (trên schema taxi) |
| Chỉ số | Execution Accuracy (EX) theo **script chấm chính thức** của benchmark | pass/fail theo nhóm |
| So sánh | **Tỷ lệ của mình vs leaderboard công khai** (đúng ý thầy) | (không cần SOTA) |
| Trạng thái | **CHƯA CÓ — phải làm mới** | **ĐÃ CÓ** ([agent-evaluation-results.json](../agent-evaluation-results.json)) |

### 3.2 Đánh giá (A) — Tỷ lệ sinh SQL trên benchmark công khai, so với leaderboard *(theo đúng ý thầy)*

**Ý thầy:** test trên **một bộ dữ liệu công khai mà người ta đã chạy & công bố điểm**, rồi
xem **tỷ lệ sinh SQL của mình so với họ** ra sao. Bộ chuẩn ngành đúng nghĩa này là
**Spider** (phổ biến nhất, có leaderboard công khai) hoặc **BIRD** (khó hơn, sát thực tế).

**Một điểm kỹ thuật phải hiểu & nói rõ trong báo cáo:**
Hệ thống đầy đủ của đồ án bị **khóa vào schema taxi + guardrails**, nên **không thể chạy
nguyên trạng** trên 200 cơ sở dữ liệu của Spider. Thứ **chạy được** trên Spider là
**module sinh SQL** (bộ Text-to-SQL dùng LLM, khi được cấp schema bất kỳ). Vì vậy:

> Ta đánh giá **năng lực sinh SQL** của đồ án **trên cùng benchmark Spider**, chấm bằng
> **script chính thức**, rồi đặt cạnh **leaderboard công khai**. Đây là so sánh
> *cùng thước đo, cùng dữ liệu* — đúng cái thầy muốn. Guardrails & deterministic planner
> là phần **đặc thù miền**, không thuộc phạm vi Spider (nói rõ ở threats to validity).

#### Các bước thực hiện
1. **Lấy dữ liệu Spider dev** (công khai): cặp *(câu hỏi, schema, SQL chuẩn)* + database SQLite.
   Để kiểm soát chi phí API, có thể chấm trên **toàn bộ dev (~1034 câu)** hoặc **mẫu 200–300 câu**
   *(nếu lấy mẫu phải nói rõ và chọn ngẫu nhiên có seed)*.
2. **Cho module sinh SQL của đồ án sinh SQL** cho từng câu (cấp schema Spider qua prompt
   — chính là `text_to_sql.generate_sql_with_openai`, bỏ qua phần catalog/guardrails taxi).
3. **Chấm bằng script chính thức của Spider** (Execution Accuracy + Exact Set Match) trên
   SQLite — **không tự chế cách chấm** để số liệu so được với người ta.
4. **So với leaderboard công khai**: lập bảng *Hệ của tôi (gpt-4o / gpt-4o-mini) vs các hệ
   công bố*. **Trích dẫn nguồn + năm** cho mọi số của người khác (số thay đổi liên tục;
   Spider top hiện ~85–91% EX, BIRD top ~65–73% — **phải tra lại lúc viết, không chép số ở đây**).
5. **Báo cáo trung thực:** nêu rõ hệ của đồ án là **zero/few-shot dùng LLM thương mại**,
   nhiều hệ trên leaderboard được **fine-tune chuyên cho Spider** → nếu mình thấp hơn là
   bình thường; mục tiêu là **định vị** chứ không phải đứng đầu.

#### (Bổ trợ) Đánh giá trên chính miền taxi — bộ taxi-nl2sql
Spider đo *năng lực sinh SQL chung*. Để đo **hệ thống thực tế đang triển khai** (có guardrails),
xây thêm bộ **taxi-nl2sql** ~**60–100 cặp** NL→SQL trên 8 bảng Gold (đủ 2 bề mặt, 3 mức khó,
Việt + Anh), chạy thật trên DuckDB để chốt kết quả, rồi đo **EX** và **so giữa các cấu hình**
của agent (deterministic / gpt-4o-mini / gpt-4o). Phần này trả lời câu "trong miền của em,
hệ chạy đúng bao nhiêu %".

> **Tóm lại:** Spider = so với người ngoài (ý thầy); taxi-nl2sql = đo hệ thống trong miền của mình.
> Hai bộ bổ sung cho nhau, nên làm cả hai.

### 3.3 Đánh giá (B) — Bộ test riêng 27 ca (đã có)
- Giữ nguyên 27 ca: **13 answer / 3 clarification / 11 blocked = 27/27 PASS**.
- Bổ sung bảng pass/fail chi tiết từng ca (case_id, surface, kỳ vọng, kết quả) — đưa Phụ lục.

### 3.4 Bảng thông số đầy đủ cho Ch.4 (chứng minh "hệ thống tốt")

| Trục | Chỉ số | Giá trị hiện có | Nguồn |
|---|---|---|---|
| Chất lượng dữ liệu | dbt tests | 77 PASS / 2 WARN / 0 ERROR | data-quality-report |
| | Lọc Bronze→Silver (2024-H1) | 20.671.900 → 20.354.795 (loại 1,53%) | data-quality-report |
| Hành vi agent | Pass rate | 27/27 (100%) | agent-evaluation-results |
| | unsafe_rejection / grounded / trace | 1.0 / 1.0 / 1.0 | nt |
| Hiệu năng | latency mart vs star (p50) | 715ms vs 1111ms | nt |
| | benchmark P01–P05 | mart ~1s, fact-join ~3,7–4,1s | performance-report |
| **Sinh SQL (MỚI)** | **EX / EM / valid-rate** | **CHƯA ĐO** | taxi-nl2sql (mới) |
| | **So sánh giữa các mô hình** | **CHƯA ĐO** | nt |

### 3.5 Threats to validity (bổ sung cho phần mới)
- Bộ taxi-nl2sql do tác giả tự gán nhãn → selection bias (đã quen với các hạn chế ở
  [evaluation-methodology.md](../thesis/evaluation-methodology.md) §7).
- So sánh với SOTA chỉ mang tính **bối cảnh** do khác benchmark/setting.
- EX dựa trên trùng kết quả, có thể "đúng kết quả nhưng SQL chưa tối ưu".

---

## 4. Công việc cần làm (checklist theo giai đoạn)

### Giai đoạn 1 — Tái cấu trúc văn bản (chủ yếu cắt/dán + viết nối)
- [ ] Dựng khung 4 chương + mục lục mới.
- [ ] Di chuyển nội dung theo Bảng mục 2.
- [ ] Viết đoạn chuyển tiếp đầu/cuối mỗi chương.
- [ ] Áp dụng [chuong3-sua-loi.md](chuong3-sua-loi.md) cho phần cài đặt (nay là Ch.4).
- [ ] Cập nhật toàn bộ tham chiếu chéo "Chương X" và đánh số hình/bảng.

### Giai đoạn 2 — Bổ sung lý thuyết Ch.2
- [ ] Viết 2.4 (Text-to-SQL, Spider/BIRD) + 2.5 (guardrails) — nền cho benchmark Ch.4.
- [ ] Viết 2.6 (mô tả lý thuyết/vai trò từng công nghệ).
- [ ] Bổ sung tài liệu tham khảo (FastAPI, DuckDB, MinIO, Streamlit, sqlglot, OpenAI, Spider, BIRD).

### Giai đoạn 3 — Đo mới phần Agent (CODE + THỰC NGHIỆM) ⚠️ nặng nhất
**3a. Benchmark công khai Spider (so với leaderboard — ý thầy):**
- [ ] Tải Spider dev (câu hỏi + schema + SQL chuẩn + SQLite) + clone script chấm chính thức.
- [ ] Viết adapter cho `text_to_sql.generate_sql_with_openai` nhận **schema Spider** (bỏ ràng buộc catalog taxi).
- [ ] Sinh SQL cho dev set (toàn bộ ~1034 hoặc mẫu 200–300 có seed) với gpt-4o & gpt-4o-mini.
- [ ] Chấm **Execution Accuracy** bằng script chính thức; lập bảng so leaderboard (trích dẫn nguồn).

**3b. Đánh giá trong miền (taxi-nl2sql):**
- [ ] Viết bộ **taxi-nl2sql** (60–100 cặp NL→SQL chuẩn), chạy DuckDB chốt kết quả tham chiếu.
- [ ] Viết script đo EX (so kết quả gen vs chuẩn) — mở rộng từ `scripts/agent_eval.py`.
- [ ] Chạy qua các cấu hình: deterministic / gpt-4o-mini / gpt-4o; lập bảng + biểu đồ.

### Giai đoạn 4 — Viết Ch.4 đánh giá + hoàn thiện
- [ ] Viết 4.7–4.10 (phương pháp + 4 trục kết quả + benchmark agent).
- [ ] Chèn ảnh thật (8 hình cũ — xem mục D của [chuong3-sua-loi.md](chuong3-sua-loi.md)).
- [ ] Viết 4.11 threats to validity, 4.12 kết luận chương, Kết luận chung.
- [ ] Rà soát thuật ngữ, tham chiếu, mục lục.

**Ước lượng công sức:** GĐ1–2 chủ yếu là viết (~vài ngày). **GĐ3 là phần rủi ro nhất**
(xây gold set + harness + chạy nhiều model + chi phí API) — nên bắt đầu sớm.

---

## 5. Tài liệu/asset cần tạo hoặc cập nhật trong repo

| File | Trạng thái | Việc |
|---|---|---|
| `benchmarks/spider/` (đề xuất) | tạo mới | dữ liệu Spider dev + script chấm chính thức |
| `scripts/spider_gen.py` (đề xuất) | tạo mới | adapter sinh SQL trên schema Spider + xuất file dự đoán |
| `scripts/run_spider_eval.*` (đề xuất) | tạo mới | gọi script chấm EX chính thức, thu kết quả |
| `docs/datasets/taxi_nl2sql.jsonl` (đề xuất) | tạo mới | bộ NL→SQL có nhãn trong miền taxi |
| `scripts/sql_accuracy_eval.py` (đề xuất) | tạo mới | đo EX trên taxi-nl2sql, nhiều cấu hình |
| `docs/sql-accuracy-report.md` (đề xuất) | tạo mới | kết quả Spider + taxi-nl2sql + bảng so leaderboard |
| [docs/thesis/evaluation-methodology.md](../thesis/evaluation-methodology.md) | cập nhật | thêm §EX trên Spider & so leaderboard |
| [docs/thesis/related-work.md](../thesis/related-work.md) | cập nhật | bổ sung Spider/BIRD + số leaderboard có trích dẫn |
| [docs/thesis/thesis-outline.md](../thesis/thesis-outline.md) | cập nhật | đổi sang khung 4 chương |

---

## 6. Quyết định cần chốt (nên hỏi lại thầy)

Đã chốt: benchmark = **bộ công khai có leaderboard** (Spider) → so tỷ lệ với người ngoài;
soạn thảo = chỉ cần kế hoạch dạng **Markdown**.

Còn mở:
1. **Spider hay BIRD?** Đề xuất **Spider** (phổ biến, dễ chấm, nhiều điểm tham chiếu).
   Hỏi thầy có chỉ định benchmark cụ thể không.
2. **Chấm toàn bộ Spider dev (~1034) hay mẫu 200–300?** (cân nhắc chi phí API).
3. **Mô hình đem so:** gpt-4o + gpt-4o-mini là tối thiểu; có thêm mô hình mở (Qwen/Llama)
   chạy local không?
4. **Ngân sách OpenAI API** (chạy ~1000 câu × nhiều model tốn token — cần xác nhận).
5. **Có làm thêm taxi-nl2sql trong miền không**, hay thầy chỉ cần phần Spider? (đề xuất: làm cả hai).

---

## 7. Rủi ro & lưu ý

- **Trên Spider:** chấm bằng **script chính thức** mới so được với leaderboard. Nhiều hệ
  top được **fine-tune riêng cho Spider**, còn đồ án dùng **LLM thương mại few-shot** →
  thấp hơn là bình thường, mục tiêu là **định vị mình ở đâu**, không phải đứng đầu.
- **Trên taxi-nl2sql:** đơn miền + schema cố định → EX cao là tất yếu; **không** được lấy
  số này so trực tiếp với leaderboard Spider (khác benchmark).
- **Chi phí & tính tái lập**: cố định seed/nhiệt độ LLM nếu được, lưu raw output để tái lập.
- **Khối lượng viết lại lớn**: ưu tiên GĐ3 (đo agent) song song với GĐ1 (cắt dán) để không dồn cuối.
- Giữ **dataset đóng băng 2024-H1** xuyên suốt để mọi số liệu nhất quán.
