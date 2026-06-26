# Kết quả đánh giá hệ thống (nguồn số cho chương Đánh giá)

Tổng hợp số liệu thực nghiệm cho đồ án. Mỗi mục ghi rõ cách đo + lệnh tái tạo.
Định vị đóng góp: **agent truy vấn an toàn, có kiểm soát, năng lực text-to-SQL cạnh tranh**
(KHÔNG claim vượt SOTA về độ chính xác). Harness: `benchmarks/`.

Model nền: `gpt-4.1-mini`. Ngày đo: 2026-06.

---

## 1. An toàn / guardrail (đóng góp lõi — Spider không đo được)
Bộ 30 truy vấn: 24 nguy hiểm (DML/DDL/lệnh/injection/bảng ngoài Gold/join trái phép/cartesian/đọc file/cột lạ/`SELECT *` bảng chi tiết) + 6 hợp lệ.

| Chỉ số | Kết quả |
|---|---|
| Chặn truy vấn nguy hiểm | **24/24 (100%)** |
| Cho qua truy vấn hợp lệ | 6/6 (100%) |
| Chặn nhầm (false positive) | **0** |

Chặn 100% ở **mọi** nhóm tấn công. → Bằng chứng định lượng cho "truy vấn an toàn, chỉ-đọc, đúng phạm vi Gold".
Tái tạo: `python benchmarks/safety/run_safety.py` (trong image `api`).

## 2. Năng lực text-to-SQL trên Spider (so với hệ khác — yêu cầu thầy #1)
Ablation: `gpt-4.1-mini` trần vs `+ lớp bọc` (guardrail + 1 lần sửa lỗi), chấm execution accuracy.

**Mẫu 80 câu (rải đều 20 DB) — sơ bộ:**
| Chế độ | exec_acc | valid | blocked |
|---|---|---|---|
| baseline | 81,2% | 100% | 0% |
| wrapped | 82,5% | 100% | 1,2% |

> Chênh lệch = 1 câu (trong nhiễu). Kết luận sơ bộ: **lớp bọc trung tính về accuracy** trên benchmark sạch + model khá — giá trị của nó ở an toàn (mục 1), không phải tăng accuracy.

**Toàn bộ 1.034 câu (CHẠY XONG 2026-06-23, wrapped-only, MỘT MÌNH):** chấm bằng bộ chính thức `test-suite-sql-eval`.
| Mức độ | Dễ | Trung bình | Khó | Rất khó | Toàn bộ |
|---|---|---|---|---|---|
| count | 248 | 446 | 174 | 166 | 1.034 |
| EX (chính thức) | 92,3% | 85,0% | 74,7% | 60,8% | **81,1%** |

- Scorer nội bộ (khắt khe thứ tự cột) = 75,3%; 99,7% truy vấn chạy được; guardrail chặn 2,8% (29 câu join ngoài FK). **Dùng 81,1%** (chuẩn leaderboard, cùng metric với hệ khác).
- Đã BỎ baseline full để tiết kiệm tiền — ablation "lớp bọc trung tính" lấy từ mẫu 80 câu ở trên.

**So sánh dev EX (cùng metric, nguồn đã xác minh) → thesis `tab:spider-compare-ch4`:**
GPT-4 0-shot 72,3 · **hệ đồ án 81,1** · GPT-4 5-shot 82,4 · DAIL-SQL 83,1 · DAIL-SQL+SC 83,6 (nguồn: repo chính chủ DAIL-SQL \cite{dail-sql}).
Bối cảnh TEST leaderboard (ghi rõ test≠dev): C3 82,3 \cite{c3-sql} · DIN-SQL 85,3 \cite{din-sql} · DAIL-SQL ~86,6 · CHASE-SQL ~87,6 \cite{chase-sql}.
→ Hệ đồ án 81,1% (gpt-4.1-mini, gần zero-shot + grounding + guardrail): **trên GPT-4 zero-shot, tiệm cận GPT-4 few-shot / DAIL-SQL**. KHÔNG claim vượt SOTA; đóng góp lõi = an toàn (mục 1, Spider không đo).
**ĐÃ đưa vào .tex:** Chuong3-4.tex §"Đánh giá trên benchmark công khai Spider" (2 bảng: độ khó + so sánh) + 4 `\bibitem` (din-sql/dail-sql/c3-sql/chase-sql) ở main.tex + cập nhật Chuong4 method (lines ~28,43). Tái lập eval chính thức: `benchmarks/spider/run_official_eval.sh` (cài tạm nltk/func_timeout/sqlparse trong container --rm).

**Phát hiện phụ (tiền kiểm guardrail trên câu gold Spider):** sau khi chuẩn hóa hoa/thường,
guardrail chấp nhận 72,5% câu gold; loại artifact dấu nháy kép thì trần thực tế ~93%.
Hai giới hạn THẬT của guardrail mà Spider phơi ra: **không hỗ trợ phép tập hợp**
(INTERSECT/UNION/EXCEPT, ~76 câu) và **join ngoài foreign key** (~26 câu) → đưa vào "hạn chế".
Tái tạo: `python benchmarks/spider/preflight.py`.

## 3. Độ chính xác trên domain taxi (yêu cầu thầy #2)
**Bộ đánh giá: 96 câu hỏi–SQL tự xây** trên Gold taxi (19 dễ / 56 trung / 21 khó). Mỗi câu có
gold SQL đã xác minh chạy được + ra kết quả trên kho (96/96, qua `verify_questions.py`). Agent thật
(planner luật + LLM fallback + guardrail + thực thi) trả lời, chấm execution accuracy **tự động**.

**Cách chấm (chuẩn execution-accuracy, kiểu Spider) — `benchmarks/taxi/scoring.py`:**
- So **kết quả**, **bỏ qua tên cột** (agent hay đặt alias/thừa cột khác gold) — đây là lý do bản chấm
  cũ "theo tên cột" chỉ ra 7,5% (đánh giá oan agent).
- So số theo **dung sai tương đối** (`math.isclose`), KHÔNG làm tròn cứng — tránh lệch dấu phẩy động
  khi SUM số lớn (vài tỷ) bị chấm sai dù giá trị đúng.
- Chỉ xét **thứ tự** khi truy vấn là xếp hạng (ORDER BY + LIMIT); ORDER BY thường coi như tập không thứ tự.
- Lưu cả rows → chấm lại offline không cần Docker/API: `python benchmarks/taxi/rescore.py`.

**Kết quả (2026-06-23, 96 câu, gpt-4.1-mini):**
| Nhóm | Accuracy |
|---|---|
| **Tổng** | **75/96 = 78,1%** |
| Dễ | 18/19 = 94,7% |
| Trung bình | 40/56 = 71,4% |
| Khó | 17/21 = 81,0% |
| Trả lời (không clarify/lỗi) | 91/96 = 94,8% |

Nguồn sinh SQL: planner luật 58, LLM 33, lỗi 5. (Đường LLM non-deterministic → dao động ±vài câu giữa các lần chạy.)

**Agent đã được nâng cấp (so với bản "planner thô" cũ ~45%) — các cải tiến THẬT, không nới lỏng chấm điểm:**
1. Đọc Top-N / cực trị đơn ("top 5", "… nào … nhất") → áp `LIMIT N` / `LIMIT 1`.
2. Xếp hạng theo đúng metric câu hỏi (doanh thu / quãng đường), không cố định `trip_count`.
3. Lọc loại dịch vụ (taxi xanh/vàng → `service_type`); lọc tháng cụ thể ("tháng N năm YYYY").
4. Phân biệt **"tháng cụ thể" = bộ lọc** với **"theo từng tháng" = chiều gom** (trước đây gom nhầm mọi câu có chữ "tháng").
5. Định tuyến đúng mức **borough** (không gom xuống zone); template vendor có thêm cột avg quãng đường / cước.
6. Prompt LLM: thêm `LIMIT` cho top-N/cực trị kể cả truy vấn tổng hợp.

Tiến trình trên cùng bộ câu: 7,5% (bug chấm theo tên cột) → 40% (sửa chấm) → 57,5% → 72,9% → **78,1%** (các fix agent).

**Hạn chế còn lại (21 câu sai — vật liệu cho mục "Hạn chế & hướng phát triển"):**
- **Gom theo chiều thời gian dẫn xuất** (quý, thứ trong tuần) hoặc cột tên-loại-dịch-vụ: LLM sinh join
  ngoài đường ngữ nghĩa cho phép → guardrail chặn (5 câu: id24,25,46,93,94). Cần bổ sung cột/đường join cho `dim_date`.
- **Câu cần MỘT số tổng** nhưng planner vẫn gom theo nhóm (tổng toàn thành phố, đếm distinct, lọc theo 1 borough cụ thể) (4 câu: id35,40,60,87).
- **Đại lượng vô hướng đặc biệt**: trung bình thật vs trung-bình-của-trung-bình, MAX, tỉ lệ phần trăm (7 câu: id11,15,29,32,34,79,80).
- **Gom hai chiều theo tháng** (hãng×tháng, thanh toán×tháng) và so sánh đón–trả không suy ra được N (3 câu: id26,27,28).
- 2 ca cận biên (id47 xếp hạng tháng, id90 vendor theo quãng đường TB).

Tái tạo: `docker compose up -d minio` rồi
`docker compose run --rm -v "${PWD}:/work" -w /work -e PYTHONPATH=/work/services/api api python benchmarks/taxi/taxi_runner.py --db /work/warehouse/analytics.duckdb`.

## 4. Hiệu năng lakehouse (yêu cầu thầy #3)
Đo độ trễ truy vấn trên kho (1 kết nối read-only, warm cache, 7 lần/câu lấy trung vị) trên
toàn bộ 40 câu domain taxi. Kho: **>98 triệu bản ghi, file DuckDB ~4,2 GB**. Ngày đo 2026-06-22.

**Tổng thể (trung vị độ trễ mỗi câu):**
| Chỉ số | Giá trị |
|---|---|
| p50 | **185,5 ms** |
| p95 | **1.314 ms** |
| trung bình | 424 ms |
| chậm nhất | 3.342 ms (câu tổng hợp fact nặng) |

→ **Độ trễ cỡ tương tác** (đa số câu < 0,2 s, 95% < 1,3 s) trên kho ~98 triệu bản ghi → đủ phục vụ truy vấn hỏi-đáp thời gian thực.

**Theo độ khó (trung vị):** dễ ~139 ms · trung bình ~160 ms · khó ~503 ms → tăng đều theo độ phức tạp truy vấn.

**Theo đường truy cập:** aggregate mart (n=14) **166 ms** vs star-schema/join fact (n=26) **188 ms** — **gần như ngang nhau**.
> Phát hiện trung thực: ở quy mô này, engine cột của DuckDB xử lý join star-schema 98 triệu dòng tốt, **mart KHÔNG nhanh hơn đáng kể** ở trung vị. Độ phân tán chủ yếu do *hình dạng truy vấn* (lượng fact phải quét/gộp), không do mart-vs-join. Giá trị của mart ở đây là **tiện ngữ nghĩa + nhất quán chỉ số**, không phải tốc độ thô. (Câu nhanh nhất 2–17 ms là tra cứu dimension/điểm; chậm nhất là gộp fact nặng.)

Tái tạo: `docker compose up -d minio` rồi chạy trong image `api`:
`python benchmarks/perf/query_latency.py --db /work/warehouse/analytics.duckdb --runs 7`
(chi tiết mỗi câu: `benchmarks/perf/latency_results.json`).

### 4b. Khả năng chịu tải (load test — mô phỏng nhiều người dùng đồng thời)
Mỗi người dùng = 1 luồng có **kết nối read-only riêng**. Quét số người dùng trên máy **12 nhân**,
đo throughput (truy vấn/giây) + độ trễ p50/p95/p99. Ngày đo 2026-06-22. Chi tiết: `benchmarks/perf/load_results*.json`.

**(a) Đông người dùng GIỐNG THẬT — mỗi người "nghĩ" ~4 s giữa các truy vấn (như analyst đọc dashboard):**
| Số người đồng thời | Throughput (q/s) | p50 | p95 |
|---|---|---|---|
| 10 | 2,2 | 128 ms | 632 ms |
| 20 | 4,3 | 136 ms | 1,2 s |
| 50 | 9,3 | 202 ms | 4,5 s |
| 100 | 8,4 | 6,4 s | 16,7 s |

→ **Thoải mái tới ~20 người dùng tương tác đồng thời** (p50≈0,13 s, p95≈1,2 s); tới ~50 người trung vị
vẫn nhanh (0,2 s) nhưng đuôi p95 bắt đầu căng → **gần ngưỡng**; 100 người bấm liên tục thì quá tải
(tải đến ≈25 q/s vượt trần ~14 q/s) → độ trễ dồn ứ. **Vùng vận hành thực tế: 20–50 người đồng thời.**

**(b) Trần bão hòa (đóng vòng, KHÔNG thời gian nghĩ — mỗi luồng bắn liên tục, để tìm giới hạn):**
truy vấn nhẹ đạt trần **~14–15 q/s**; vượt mức tối ưu thì throughput đi ngang rồi giảm nhẹ, độ trễ
tăng dần — **không sập/không lỗi** (C=8→16→32→64: 13,5 → 14,4 → 15,3 → 11,9 q/s).
Theo định luật Little, trần ~14 q/s với think-time 4 s ≈ **~60 người**, với 30 s ≈ **vài trăm người** dùng bình thường.

**(c) Tải phân tích nặng (toàn bộ 40 câu, gồm vài câu gộp fact 1,8–3,3 s):**
| Đồng thời | Throughput (q/s) | p50 | p95 | p99 |
|---|---|---|---|---|
| 1 | 2,0 | 333 ms | 1,4 s | 3,8 s |
| 8 | 4,4 | 1,1 s | 4,7 s | 9,3 s |
| 16 | **5,3** | 2,2 s | 7,6 s | 9,9 s |

→ Throughput chạm trần ~5 q/s; độ trễ suy giảm **mượt** (không sập, không lỗi) khi tải tăng.

**Diễn giải trung thực (đặc tính đúng của OLAP):** mỗi truy vấn DuckDB đã dùng hết 12 nhân,
nên tăng số người dùng làm **throughput bão hòa nhanh, độ trễ tăng dần** — đây là engine
**phân tích thiên về throughput-mỗi-truy-vấn**, KHÔNG phải kho OLTP high-QPS. Capping luồng/kết
nối (thử `--threads 2`) không nâng được trần (~4,6 q/s) vì nút cổ chai là các câu gộp fact nặng.
→ Kết luận: lakehouse **dư sức cho tải hỏi-đáp/BI thực tế** (chục người đồng thời, độ trễ dưới giây),
và **xuống cấp có kiểm soát** dưới tải phân tích nặng — đúng kỳ vọng của một kho phân tích.

Tái tạo: `python benchmarks/perf/load_test.py --db /work/warehouse/analytics.duckdb --levels 1,2,4,8,16 --duration 20`
(thêm `--ids ...` để chạy riêng tải dashboard, `--think-ms N` để mô phỏng người dùng có thời gian nghĩ, `--threads N` để giới hạn luồng/kết nối).

### 4c. Độ trễ cold-cache (truy vấn đầu, tiến trình mới)
Tiến trình DuckDB mới mở kho 4,26 GB, đo lần chạy ĐẦU mỗi câu (không warm-up). So với §4 (warm):
| | p50 | p95 | trung bình |
|---|---|---|---|
| Cold (lần đầu) | 300 ms | 1,28 s | 537 ms |
| Warm (§4) | 185 ms | 1,31 s | 424 ms |

→ Phí khởi động nguội ~**1,6×** ở trung vị (mở kho + đọc trang lần đầu), nhưng **vẫn dưới giây**; sau câu đầu vào warm. Tái tạo: `query_latency.py --no-warmup --runs 1`.

### 4d. Thông lượng pipeline (ingestion + transform — yêu cầu thầy #3)
Nguồn: metadata 3 lần chạy `taxi_monthly_pipeline` (`data/metadata/pipeline_runs/`) + `dbt/target/run_results.json`.
Kho hiện có **fact_trips ≈ 105,9 triệu chuyến** (silver_trips_unified cùng cỡ).

- **Một lần chạy pipeline tháng** (ingestion-check → bronze → silver → gold, **12 model dbt** cùng bộ kiểm thử chất lượng; dbt build báo cáo **PASS=77 / WARN=2** tính cả model và test): **~2 phút wall-clock**.
- **Bronze+Silver ~85 s:** silver `+materialized: table` → **dựng lại toàn bộ bảng 106 triệu dòng mỗi lần** ⇒ thông lượng transform **≳1 triệu dòng/giây**.
- **Gold ~20–37 s:** gold `+materialized: view` (tính khi đọc) + chạy 61 test chất lượng. Test nặng nhất là kiểm toàn vẹn fact/gold quét full bảng (3–8 s/test): `not_null_gold_zone_demand_*`, `relationships_fact_trips_*`.
- **Chất lượng dữ liệu chạy mỗi lần:** ~63 dbt test (not_null, quan hệ khóa, assert tùy biến) **PASS** → pipeline tự kiểm, không chỉ nạp.
- Ghi chú thiết kế (trung thực): ingestion **tăng dần theo tháng** (tải 1 tháng, bỏ qua file đã có) nhưng silver **dựng lại toàn bộ** mỗi lần → muốn mở rộng nhiều năm nên chuyển silver sang incremental.

### 4e. Hiệu quả lưu trữ
| Lớp | Dung lượng | Trên 106 tr chuyến |
|---|---|---|
| Lake bronze (parquet, MinIO) | **1,8 GB** | ~18 byte/chuyến |
| Kho phục vụ (DuckDB native) | **4,26 GB** | ~40 byte/chuyến |

→ Parquet nén cột rất gọn: 1,8 GB cho 106 triệu chuyến (1 tháng yellow ~3 tr dòng = ~50 MB), **~7–8× nhỏ hơn CSV thô tương đương** (~14 GB). Kho DuckDB lớn hơn lake vì chứa bảng silver materialized + star-schema dim, đổi dung lượng lấy tốc độ truy vấn.

---

## Việc mai làm tiếp (resume 2026-06-18)
1. ✅ **Spider full 1.034 — XONG 2026-06-23** (wrapped-only, MỘT MÌNH, qua PowerShell vì Bash mangle `-w /work`). Bộ chấm chính thức = **81,1% EX** (bảng theo độ khó đã ở mục 2). Đã vào thesis. Tái lập: `benchmarks/spider/run_official_eval.sh`.
2. ✅ **Đo hiệu năng (mục 4) — XONG 2026-06-22:** p50=185 ms, p95=1.314 ms; mart≈star (166 vs 188 ms). Số đã điền mục 4.
3. ✅ **Đã chọn (B):** cải tiến agent + sửa scorer + mở rộng 96 câu → taxi 78,1% (mục 3); Spider full → 81,1% (mục 2). Tất cả đã đưa vào .tex.

## Khung định vị cho báo cáo (chốt)
- **Đừng** viết "vượt trội/chính xác hơn SOTA".
- **Nên** viết: hệ thống cung cấp **truy vấn an toàn có kiểm soát (mục 1: chặn 100%)**,
  **năng lực text-to-SQL cạnh tranh (mục 2: Spider full dev 81,1%, trên GPT-4 zero-shot, tiệm cận GPT-4 few-shot/DAIL-SQL, model nhỏ + rẻ + có guardrail)**, **đúng trên domain
  thật (mục 3)**, **hiệu năng đủ phục vụ truy vấn tương tác (mục 4)**.
- Hạn chế (trung thực): guardrail chưa hỗ trợ phép tập hợp và join ngoài FK; accuracy phụ
  thuộc model nền; phạm vi Gold/đọc-only.

---

## Insight dashboard 2024-H1 (xác minh 2026-06-23, analytics.duckdb)
Lọc cửa sổ: `source_year=2024 AND source_month BETWEEN 1 AND 6` (= 20.354.795 chuyến, khớp tổng đã chốt).

| Chỉ tiêu | Giá trị đo | Ghi trong báo cáo (Chuong3-3.tex:197) |
|---|---|---|
| Tổng chuyến 2024-H1 | 20.354.795 | khớp |
| Yellow Taxi | 20.016.200 (98,34%) | khớp ("~98%") |
| Pickup Manhattan | 18.044.980 (88,65%) | khớp |
| Pickup Queens (cả borough) | 1.869.256 (9,18%) | khớp ("Queens 9,18%") |
| Nhóm sân bay JFK+LGA (service_zone='Airports') | 1.517.158 (**7,45%**) | đã sửa: trước ghi nhầm 9,18% cho "nhóm sân bay" |
| Doanh thu sân bay | JFK $72,5M > LGA $42,9M | khớp ("JFK dẫn đầu doanh thu") |
| Thẻ tín dụng | 15.341.141 (75,37%) | khớp ("~75,4%") |
| Tiền mặt | 2.804.774 (13,78%) | khớp ("~13,8%") |
| Quãng đường trung vị / trung bình | 1,76 / 4,88 dặm | khớp ("trung vị ~1,8; trung bình cao hơn do ngoại lai") |

Kết luận: mọi số insight là THẬT, chỉ 1 chỗ gán nhãn sai (9,18% là Queens cả borough, không phải riêng sân bay) đã sửa trong báo cáo.

**Bối cảnh kho (live 2026-06-23):** `fact_trips` = 105.929.974 dòng, 29 tháng 12/2023→04/2026. Báo cáo vẫn dùng snapshot đóng băng **>98 triệu / đến 03/2026** (không dùng số live).
