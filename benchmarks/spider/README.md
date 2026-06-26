# Spider benchmark harness

Chạy lớp bọc Text-to-SQL (gpt-4.1-mini + semantic catalog + guardrail `validate_gold_select`)
trên bộ Spider của người ta, rồi chấm điểm để **so sánh** — đúng yêu cầu GVHD.

Hai chế độ (ablation):
- **baseline** — gpt-4.1-mini sinh SQL từ schema thô. Không guardrail, không sửa lỗi.
- **wrapped** — cùng model, prompt có grounding theo schema + guardrail + 1 lần sửa lỗi.

Hiệu `wrapped − baseline` = đóng góp của lớp bọc.

## Module
| File | Vai trò | Đã kiểm thử |
|---|---|---|
| `schema_adapter.py` | `tables.json` → `SchemaResponse` của agent | ✅ self-test (`python schema_adapter.py`) |
| `scorer.py` | Execution accuracy trên SQLite (so kết quả với gold) | ✅ self-test (`python scorer.py`) |
| `runner.py` | Sinh SQL (baseline/wrapped) → guardrail → chấm → tổng hợp | cần dataset + API key |

## 1. Tải Spider 1.0
Trang chính: https://yale-lily.github.io/spider (tải qua Google Drive).
Giải nén, cần 3 thứ:
```
spider/
  dev.json          # 1.034 câu: {db_id, question, query}
  tables.json       # schema mọi DB
  database/<db_id>/<db_id>.sqlite   # các DB SQLite để thực thi
```

Để **so số chính danh với leaderboard**, tải thêm bộ chấm chính thức
(taoyds/test-suite-sql-eval) và chạy nó song song với scorer nhẹ trong repo này.

## 2. Chạy
Chạy trong container `api` (có sẵn `openai` + `sqlglot`); đảm bảo thư mục `spider/`
nằm trong đường dẫn mount được và đặt `OPENAI_API_KEY`.

```bash
# smoke-test 50 câu trước cho rẻ
python benchmarks/spider/runner.py \
  --dev spider/dev.json --tables spider/tables.json --db-dir spider/database \
  --mode both --limit 50 --out benchmarks/spider/results_smoke.json

# chạy đầy đủ 1.034 câu
python benchmarks/spider/runner.py \
  --dev spider/dev.json --tables spider/tables.json --db-dir spider/database \
  --mode both --out benchmarks/spider/results.json
```
In ra bảng: `mode | n | exec_acc | valid_rate | blocked`, và ghi kết quả từng câu
(gold, pred, lỗi) ra JSON để **phân loại lỗi** thủ công sau.

Chi phí: gpt-4.1-mini rất rẻ — toàn bộ 1.034 câu × 2 chế độ chỉ vài đô. Cứ `--limit 50` thử trước.

## 3. So sánh với ai
- Cột "cùng điều kiện": **baseline** (gpt-4.1-mini trần) — chính là trong kết quả này.
- Cột "hệ khác": số công bố trên **cùng Spider dev** (DIN-SQL, CHASE-SQL, MARS-SQL…).

## Quyết định thiết kế & lưu ý trung thực (phải ghi trong báo cáo)
1. **Bỏ qua deterministic planner taxi** trong `app.agent`: nó chỉ phủ domain taxi,
   sẽ sinh SQL taxi sai cho câu Spider. Harness đo năng lực text-to-SQL tổng quát
   (LLM + guardrail) — phần thực sự khái quát hóa được.
2. **Mọi bảng benchmark = `aggregate_mart` + `execution_enabled`** để guardrail cho phép
   `SELECT *` (Spider dùng nhiều) và không loại bảng.
3. **`allowed_joins` sinh từ foreign key** của benchmark — bản tương đương của join
   path được curate trong catalog taxi. ⚠️ Câu Spider join ngoài FK sẽ bị guardrail
   chặn → kéo accuracy `wrapped` xuống ở câu nhiều bảng. Đây là guardrail hoạt động
   đúng thiết kế; nêu rõ trong phần thảo luận.
4. **Không cắt LIMIT**: đặt `max_rows` cực lớn để guardrail không chèn LIMIT làm lệch
   kết quả; thực thi câu SQL gốc của LLM trên SQLite (đúng dialect benchmark).
5. **scorer.py là bản nhẹ** (so multiset, có xét ORDER BY). Để có số so trực tiếp với
   bảng xếp hạng, chạy thêm bộ chấm test-suite chính thức.
6. ⚠️ **Phân biệt hoa/thường**: guardrail so tên bảng/cột bằng chuỗi chính xác. Nếu
   schema Spider và SQL sinh ra lệch hoa/thường có thể bị chặn nhầm — kiểm tra khi
   smoke-test 50 câu, nếu gặp thì hạ về lowercase ở cả hai phía.
