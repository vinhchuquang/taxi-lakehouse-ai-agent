# Documentation Index

Hai nhóm tài liệu chính trong thư mục này:

- **Tài liệu kỹ thuật và vận hành** — phục vụ phát triển và vận hành hệ thống.
- **Tài liệu báo cáo tốt nghiệp** — nằm trong [`thesis/`](thesis/), phục vụ
  viết báo cáo và bảo vệ.

> Xem hướng dẫn tổng thể về dự án ở [`../CLAUDE.md`](../CLAUDE.md) và
> [`../AGENTS.md`](../AGENTS.md).

---

## 1. Kiến trúc và thiết kế

| File | Mục đích |
|---|---|
| [architecture.md](architecture.md) | Kiến trúc tổng thể, thành phần, luồng dữ liệu |
| [architecture-review.md](architecture-review.md) | Review kiến trúc và quyết định thiết kế |
| [modeling-decisions.md](modeling-decisions.md) | Lý do chọn star schema cho Gold |
| [gold-star-schema.md](gold-star-schema.md) | Chi tiết fact + 5 dimension + 2 aggregate marts |
| [data-contracts.md](data-contracts.md) | Hợp đồng dữ liệu Bronze/Silver/Gold/Agent |
| [source-notes.md](source-notes.md) | Ghi chú về nguồn dữ liệu TLC |

## 2. Vận hành và phát triển

| File | Mục đích |
|---|---|
| [runbook.md](runbook.md) | Quy trình khởi động, build, verify |
| [development-roadmap.md](development-roadmap.md) | Roadmap 41 phases với verification dates |
| [release-checklist.md](release-checklist.md) | Checklist trước mỗi lần release |
| [security-notes.md](security-notes.md) | Lưu ý an ninh khi vận hành local |
| [codex-agent-playbook.md](codex-agent-playbook.md) | Playbook cho AI agent (Codex) sửa code |

## 3. Đánh giá và báo cáo kết quả

| File | Mục đích |
|---|---|
| [agent-evaluation.md](agent-evaluation.md) | Phương pháp + cấu trúc bộ test agent |
| [agent-evaluation-results.json](agent-evaluation-results.json) | Snapshot kết quả 27/27 cases PASS |
| [data-quality-report.md](data-quality-report.md) | Báo cáo dbt tests 77/2/0/0 + anomaly |
| [performance-report.md](performance-report.md) | Benchmark 5 query đại diện |
| [performance-benchmark-results.json](performance-benchmark-results.json) | Snapshot benchmark JSON |
| [test-results-report.md](test-results-report.md) | Tổng kết pytest và verification |
| [demo-scenarios.md](demo-scenarios.md) | 12 demo scenarios cho buổi bảo vệ |

## 4. Tài liệu báo cáo tốt nghiệp

→ Toàn bộ vật liệu để viết báo cáo và làm slide nằm trong [`thesis/`](thesis/).
Bắt đầu từ [`thesis/README.md`](thesis/README.md).

| File chính | Vai trò |
|---|---|
| [thesis/thesis-outline.md](thesis/thesis-outline.md) | Đề cương 6 chương báo cáo |
| [thesis/thesis-chapter-templates.md](thesis/thesis-chapter-templates.md) | Đoạn văn mẫu cho từng chương |
| [thesis/abstract.md](thesis/abstract.md) | Tóm tắt/Abstract song ngữ |
| [thesis/related-work.md](thesis/related-work.md) | 31 references nhóm theo chủ đề |
| [thesis/architecture-diagrams.md](thesis/architecture-diagrams.md) | 7 sơ đồ Mermaid |
| [thesis/evaluation-methodology.md](thesis/evaluation-methodology.md) | Phương pháp đánh giá chính thức |
| [thesis/production-roadmap.md](thesis/production-roadmap.md) | Hướng phát triển sau bảo vệ |
| [thesis/figures-and-tables-index.md](thesis/figures-and-tables-index.md) | Danh mục hình/bảng/đoạn mã |
| [thesis/glossary.md](thesis/glossary.md) | Từ điển thuật ngữ Việt-Anh |
| [thesis/defense-presentation.md](thesis/defense-presentation.md) | Slide outline + Q&A bảo vệ |
