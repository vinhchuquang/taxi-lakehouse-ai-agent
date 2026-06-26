# Slide Bảo vệ và Q&A

Outline slide cho buổi bảo vệ (gợi ý ~18 slide, trình bày 12–15 phút) kèm
**ngân hàng câu hỏi & trả lời** dự đoán hội đồng có thể hỏi.

- Thời gian khuyến nghị: 12–15 phút trình bày + 10–15 phút Q&A.
- Demo trực tiếp (nếu hội đồng cho phép): xem [demo-scenarios.md](../demo-scenarios.md).
- Số liệu trong các slide lấy từ [agent-evaluation-results.json](../agent-evaluation-results.json)
  (Phase 37). Cập nhật nếu chạy lại đánh giá.

---

## A. Outline 18 slide

### Slide 1 — Bìa
- Tên đề tài: **[TÊN ĐỒ ÁN ĐẦY ĐỦ]**
- Sinh viên thực hiện: [HỌ VÀ TÊN], MSSV [XXXX]
- Giảng viên hướng dẫn: [TÊN GVHD]
- Trường / Khoa / [NĂM]

### Slide 2 — Nội dung trình bày
1. Bối cảnh và mục tiêu
2. Cơ sở lý thuyết
3. Thiết kế hệ thống
4. Triển khai
5. Đánh giá
6. Kết luận và hướng phát triển

### Slide 3 — Bối cảnh và động lực
- Dữ liệu TLC: ~hàng trăm triệu chuyến/năm, công khai.
- Hai xu hướng giao thoa: **Lakehouse** và **AI agent**.
- Vấn đề: agent Text-to-SQL cần **guardrails an toàn**, hầu hết khung hiện
  có giấu workflow → khó kiểm chứng.

### Slide 4 — Mục tiêu và phạm vi
- 4 mục tiêu: pipeline, star schema, agent đọc-only, đánh giá định lượng.
- **Trong phạm vi**: Yellow + Green, 2024-H1, local-first.
- **Ngoài phạm vi**: FHV/HVFHV, streaming, write-agent, cloud.

### Slide 5 — Cơ sở lý thuyết (1 slide tổng kết)
- Lakehouse + Medallion (Bronze/Silver/Gold).
- Kimball star schema.
- Text-to-SQL + LLM agent + guardrails.
- → Chi tiết ở [related-work.md](related-work.md).

### Slide 6 — Kiến trúc tổng thể
- Chèn Hình 1 từ [architecture-diagrams.md](architecture-diagrams.md).
- 7 service Docker: MinIO, Airflow (×3), API, Demo, Postgres.

### Slide 7 — Luồng dữ liệu Bronze → Silver → Gold
- Chèn Hình 2.
- Bronze: raw + checksum. Silver: 1 model unified, validity filters loại
  ~18M dòng. Gold: 1 fact + 5 dim + 2 mart.

### Slide 8 — Star schema Gold
- Vẽ sơ đồ `fact_trips` ở trung tâm, 5 dimension xung quanh.
- Nêu rõ join keys và một số metric chính.

### Slide 9 — Agent state machine
- Chèn Hình 3.
- 7 trạng thái: Intent → Plan → SQL → Guardrails → Execute → Self-check →
  Answer.
- Nhấn mạnh: **deterministic answer là mặc định**.

### Slide 10 — Hệ guardrails 3 tầng
- Chèn Hình 4.
- 3 tầng: column / table / join.
- Công cụ: `sqlglot` parse AST, không dùng regex.

### Slide 11 — Triển khai (highlight)
- 12 dbt models, 77/2/0 tests.
- DAG `taxi_monthly_pipeline`, metadata bền vững Phase 25.
- FastAPI 3 endpoints, Streamlit 4 tab.

### Slide 12 — Demo (chia 2 slide hoặc demo trực tiếp)
- Mở Streamlit, chạy 2–3 câu hỏi:
  1. "Tổng số chuyến yellow trong tháng 1/2024 theo vendor" → answer.
  2. "Cho tôi xem toàn bộ fact_trips" → blocked (wildcard).
  3. Câu mơ hồ → clarification.
- Chỉ vào `agent_steps` để chứng minh trace.

### Slide 13 — Đánh giá: phương pháp
- 3 trục: Data quality, Agent correctness/safety, Performance.
- Dataset cố định `2024-H1` để tái lập.
- 27 cases hồi quy (13 + 3 + 11).

### Slide 14 — Kết quả: data quality + agent
- dbt: **77 PASS / 2 WARN / 0 ERROR**.
- Agent: **27/27 PASS** (100%).
- `unsafe_rejection_rate = 1.0`, `grounded_answer_rate = 1.0`.

### Slide 15 — Kết quả: hiệu năng
- Bảng latency: aggregate p50 715ms, star p50 1111ms, answer p95 2935ms.
- Quyết định Phase 17: giữ Gold ở dạng view.

### Slide 16 — Hạn chế (threats to validity)
- 5 hạn chế: selection bias, no external ground truth, single-turn, narrow
  window, local hardware.

### Slide 17 — Đóng góp và hướng phát triển
- 4 đóng góp chính (lặp lại từ Chương 1.4).
- Hướng phát triển ngắn: mở rộng FHV, adversarial test, multi-turn, K8s
  deployment.

### Slide 18 — Cảm ơn + hỏi đáp
- "Em xin cảm ơn hội đồng. Em sẵn sàng nhận câu hỏi."
- Có thể để sẵn 2–3 backup slide (kiến trúc chi tiết hơn, raw evaluation
  JSON, mã guardrail).

---

## B. Backup slides (khi cần)

- **B1.** Chi tiết semantic catalog YAML (1 ví dụ entry).
- **B2.** Pipeline run metadata JSON (1 ví dụ).
- **B3.** Code đoạn guardrails (10–15 dòng).
- **B4.** Toàn bộ bảng 27 cases với case_id, surface, status.

---

## C. Ngân hàng Q&A dự đoán

> Gợi ý: in phần này ra giấy, ôn 1–2 ngày trước bảo vệ. Mỗi câu trả lời nên
> **bám bằng chứng cụ thể** trong repo, không trả lời chung chung.

### C.1 Câu hỏi về phạm vi và lựa chọn công nghệ

**Q1.** Tại sao em không dùng Snowflake / BigQuery / Databricks?
> A: Đồ án định hướng *local-first*, mục tiêu thể hiện kiến trúc Lakehouse
> đầy đủ trên một máy. DuckDB + MinIO cho phép tái lập trên bất kỳ máy nào
> có Docker, không phụ thuộc tài khoản đám mây. Ngoài ra chi phí cloud cho
> dataset trăm triệu dòng là rào cản học thuật. Nếu mở rộng production thì
> em đề xuất chuyển sang Trino/Spark — đã ghi trong
> [production-roadmap.md](production-roadmap.md) §4.2.

**Q2.** Tại sao tự xây agent thay vì dùng LangChain hoặc Vanna?
> A: Hai lý do. (a) **Khả năng trace**: tự xây giúp mỗi bước trong workflow
> đều test và đo riêng được, từ đó bộ 27 cases đánh giá có thể đo từng metric
> chi tiết. (b) **Phụ thuộc abstraction**: LangChain thay đổi API thường
> xuyên, không phù hợp với một codebase tốt nghiệp cần ổn định. Quyết định
> này được ghi rõ trong [AGENTS.md](../../AGENTS.md).

**Q3.** Tại sao không làm FHV/HVFHV (Uber/Lyft)?
> A: FHV có schema và volume khác Yellow/Green đáng kể, cần model riêng cho
> Silver/Gold. Nếu cố ôm sẽ làm cả hai phần dở. Em chọn hoàn thiện một
> phạm vi nhỏ với đầy đủ guardrails và đánh giá thay vì mở rộng. Hướng phát
> triển trong [production-roadmap.md](production-roadmap.md) §1.1 đã ước
> tính khoảng 3 tuần cho phần mở rộng này.

### C.2 Câu hỏi về thiết kế dữ liệu

**Q4.** Tại sao chọn star schema mà không chọn snowflake hay 3NF?
> A: Star schema phù hợp với engine columnar (DuckDB) — ít JOIN, dễ đọc.
> Snowflake schema chia nhỏ dimension làm tăng số JOIN; 3NF phù hợp OLTP
> chứ không OLAP. Tham khảo Kimball, *The Data Warehouse Toolkit*
> [related-work #4].

**Q5.** Tại sao có cả `fact_trips` lẫn `gold_daily_kpis`, `gold_zone_demand`?
Có dư thừa không?
> A: Hai aggregate mart là **fast path** cho câu hỏi phổ biến (KPI theo
> ngày, nhu cầu theo zone). `fact_trips` mới là *flexible path* cho câu
> hỏi không nằm trong template mart. Phân chia này được ghi rõ trong
> [modeling-decisions.md](../modeling-decisions.md). Khi đánh giá hiệu năng
> (Phase 17), em thấy mart cho p50 715ms còn star schema cho p50 1111ms —
> giữ cả hai là cân bằng tốt giữa tốc độ và tính linh hoạt.

**Q6.** Anomaly trong Silver xử lý thế nào? Em có loại hết không?
> A: Không loại hết. Em phân biệt hai loại:
> - **Loại bằng validity filter**: pickup ngoài tháng partition, dropoff
>   trước pickup, amount âm, distance bất hợp lý → loại khỏi Silver
>   (~18M dòng).
> - **Giữ lại nhưng cảnh báo**: pickup ngoài tháng partition nhưng vẫn hợp
>   lệ về thời gian → dbt WARN test ghi nhận. Đây là *bất thường nguồn từ
>   TLC*, không phải lỗi pipeline.
> Lý do: thông tin về anomaly nguồn quan trọng cho người dùng nghiệp vụ.
> Chi tiết: [data-quality-report.md](../data-quality-report.md).

### C.3 Câu hỏi về agent và guardrails

**Q7.** Nếu LLM cố tình sinh SQL nguy hiểm, làm sao em chắc chắn chặn được?
> A: Em không tin LLM. Em tin AST parsing.
> - LLM chỉ sinh string SQL.
> - sqlglot parse string thành AST, kiểm 3 tầng (column/table/join).
> - Tầng 2 chặn bằng allow-list theo `execution_enabled` trong semantic
>   catalog — LLM không thể "lách".
> - Em đã xác nhận với 11 cases blocked đại diện cho 6 trục tấn công
>   khác nhau, tất cả đều bị chặn trước khi chạm DuckDB. Chi tiết trong
>   [evaluation-methodology.md](evaluation-methodology.md) §2.2.

**Q8.** Nếu user hỏi "DROP TABLE fact_trips" thì sao?
> A: Statement-type checking là tầng đầu tiên: non-SELECT bị chặn ngay
> trước cả khi parse cấu trúc bảng. Em có case test này trong harness.

**Q9.** Câu trả lời natural language do OpenAI tạo ra, có lỗi hallucination
không?
> A: Em phân biệt rõ:
> - **Deterministic answer** là mặc định, tạo từ rows thực tế (template).
> - **OpenAI synthesis** là opt-in, và bị ràng buộc phải *grounded* — chỉ
>   được tham chiếu rows đã chạy SQL trả về.
> - Trong 27 cases đánh giá, `grounded_answer_rate = 1.0`.
> Em không bao giờ để LLM tự suy ra số từ ý hiểu — số luôn phải từ DuckDB.

**Q10.** Agent có hỗ trợ hội thoại nhiều lượt (multi-turn) không?
> A: Hiện tại không. Streamlit có lưu lịch sử *hiển thị* nhưng không gửi
> ngược về API. Lý do: multi-turn cần thêm conversation store, đánh giá
> riêng cho continuity, và risk hallucination liên kết các câu hỏi không
> liên quan. Em đã liệt kê đây là hướng phát triển trong
> [production-roadmap.md](production-roadmap.md) §3.

### C.4 Câu hỏi về đánh giá

**Q11.** 27 cases có quá ít không?
> A: Số lượng nhỏ là *có chủ đích*. Mục tiêu là **coverage 3 trục guardrail**
> chứ không phải accuracy benchmark như Spider. Em chia: 13 cases positive
> (answer) chia đều 2 surface, 11 cases blocked phủ 6 trục guardrail khác
> nhau, 3 cases clarification. Đây không phải Spider — không cần thousands.
> Tuy nhiên em có ghi rõ đây là **hạn chế (selection bias)** trong báo cáo
> Chương 5.5.

**Q12.** Em có so sánh với baseline không?
> A: Hiện tại chưa có baseline so sánh chính thức (mart-only vs full
> planner, deterministic vs LLM-only). Em đã liệt kê đây là hướng phát
> triển F4 trong [production-roadmap.md](production-roadmap.md) §10.

**Q13.** Tại sao đánh giá độ chính xác câu trả lời mà không có nhãn vàng?
> A: Em đánh giá ở mức *grounded-on-rows*: câu trả lời natural language phải
> tham chiếu đúng các giá trị trong rows mà SQL trả về. Em không có
> annotator độc lập nên không claim *human-aligned accuracy*. Đây là hạn
> chế đã được ghi nhận trong [evaluation-methodology.md](evaluation-methodology.md)
> §7.

**Q14.** Hiệu năng 3 giây có ổn cho production không?
> A: Cho demo và analytics ad-hoc, *có*. Cho dashboard real-time, *không*.
> Khi đó cần materialize aggregate marts hoặc dùng caching layer. Quyết
> định trong Phase 17 là giữ view vì dataset đồ án vừa đủ. Cho production
> đa người dùng đồng thời, em đề xuất Trino/Spark.

### C.5 Câu hỏi về vận hành

**Q15.** Nếu Airflow DAG fail, em xử lý thế nào?
> A: Mỗi run ghi metadata vào MinIO với `quality_gate` rõ ràng (passed /
> passed_with_warnings / failed). Script `check_pipeline_run.py` kiểm tra
> trạng thái này. Trong production em đề xuất push metadata lên Prometheus
> và alert khi gate = failed. Chi tiết: [runbook.md](../runbook.md).

**Q16.** Nếu TLC đổi schema thì sao?
> A: Bronze giữ nguyên file gốc nên không bị ảnh hưởng. Silver có schema
> mapping — nếu TLC đổi tên cột, em chỉ cần update model `silver_trips_unified`
> và dbt sẽ báo lỗi schema. Đây là một trong các lý do để Silver là một
> tầng riêng thay vì transform trong Bronze.

**Q17.** Hệ thống có thực sự chạy được không hay chỉ là demo?
> A: `docker compose up -d` là đủ để có toàn bộ stack. 41 phases đều có
> verification date trong [development-roadmap.md](../development-roadmap.md).
> Em mời hội đồng kiểm tra trực tiếp bằng demo (slide 12) hoặc bằng việc
> chạy lại harness 27 cases.

### C.6 Câu hỏi "bẫy" thường gặp

**Q18.** Em có thể giải thích "Lakehouse" trong 1 câu không?
> A: Lakehouse là kiến trúc dữ liệu kết hợp lưu trữ chi phí thấp của data
> lake với khả năng truy vấn SQL có cấu trúc của data warehouse, thường
> được tổ chức theo ba lớp Bronze → Silver → Gold.

**Q19.** Đóng góp khoa học của đồ án là gì?
> A: Đồ án không phải nghiên cứu mới về thuật toán. Đóng góp chính là một
> **mô hình tham chiếu** đầy đủ chạy local: lakehouse + star schema + AI
> agent đọc-only với guardrails minh bạch và đánh giá tái lập được. Giá
> trị nằm ở *tính kỹ sư* (engineering rigor) và *tính giáo dục* (có thể
> dùng làm tài liệu giảng dạy).

**Q20.** Em đã học được gì từ đồ án này?
> A: «Câu này cá nhân hóa. Gợi ý:
> - Tầm quan trọng của *scope discipline* — chốt 'Do Not' từ đầu.
> - Khác biệt giữa *test code đúng* và *test feature đúng*.
> - Allow-list mạnh hơn deny-list trong an toàn agent.»

---

## D. Mẹo trình bày

1. **Mở đầu mạnh**: 30 giây đầu nói rõ "Em xây dựng X để giải quyết Y."
   Tránh kể lan man.
2. **Cứ 2–3 slide là một con số**: 77 dbt PASS, 27/27 agent PASS, 98M
   rows. Hội đồng nhớ số tốt hơn câu chữ.
3. **Demo trực tiếp tốt hơn screenshot**: nếu phòng cho phép, mở Streamlit
   trên màn hình chiếu. Backup screenshot trong slide phòng khi mạng/Docker
   trục trặc.
4. **Trả lời "em không biết" khi cần**: nếu hội đồng hỏi vượt scope, nói
   "Em chưa nghiên cứu phần này, em sẽ ghi nhận làm hướng phát triển" —
   tốt hơn là bịa.
5. **Bám vào file**: mỗi câu trả lời nên trỏ về một file trong repo. Hội
   đồng đánh giá cao việc có "vật chứng".

---

## E. Checklist trước bảo vệ

- [ ] In slide ra giấy (backup khi máy chiếu lỗi).
- [ ] Chuẩn bị laptop có Docker chạy sẵn, stack `docker compose up` đã test.
- [ ] In phần C (Q&A) làm flashcard.
- [ ] Đối chiếu số liệu slide với JSON snapshot mới nhất.
- [ ] Tập trình bày 2 lần với thời gian — phải dưới 15 phút.
- [ ] Backup 2–3 slide chi tiết (semantic catalog, code snippet, JSON eval).
- [ ] Ghi tên GVHD, hội đồng chính xác lên bìa slide.
