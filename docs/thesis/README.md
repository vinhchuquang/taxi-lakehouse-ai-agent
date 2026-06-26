# Tài liệu viết Báo cáo Tốt nghiệp

Thư mục này chứa **toàn bộ vật liệu** để viết báo cáo tốt nghiệp và chuẩn bị
buổi bảo vệ. Các tài liệu vận hành/kỹ thuật của hệ thống nằm ở thư mục mẹ
[`docs/`](../).

> Đối tượng người dùng: **sinh viên thực hiện đồ án**.
> Mục tiêu: chuyển từ "code đã xong" sang "báo cáo có thể bảo vệ" trong
> khoảng 7–10 ngày.

---

## Quy trình đề xuất

1. **Đọc trước** — [thesis-outline.md](thesis-outline.md) để có khung 6
   chương báo cáo.
2. **Soạn nháp** — copy [thesis-chapter-templates.md](thesis-chapter-templates.md)
   vào Word/LaTeX, điền `[ ]`.
3. **Chuẩn bị hình ảnh** — render Mermaid từ
   [architecture-diagrams.md](architecture-diagrams.md), chụp screenshot
   theo hướng dẫn trong [figures-and-tables-index.md](figures-and-tables-index.md).
4. **Tra thuật ngữ** — dùng [glossary.md](glossary.md) để giữ thuật ngữ
   nhất quán Việt-Anh.
5. **Viết tóm tắt** — chọn 1 bản dài + 1 bản ngắn từ [abstract.md](abstract.md).
6. **Tham khảo lý thuyết** — trích dẫn theo [related-work.md](related-work.md).
7. **Viết phần đánh giá** — bám sát [evaluation-methodology.md](evaluation-methodology.md).
8. **Viết phần future work** — dùng [production-roadmap.md](production-roadmap.md).
9. **Chuẩn bị bảo vệ** — slide + Q&A theo [defense-presentation.md](defense-presentation.md).

---

## Danh sách tài liệu

### Khung và nội dung viết

| File | Vai trò | Ngôn ngữ |
|---|---|---|
| [thesis-outline.md](thesis-outline.md) | Đề cương 6 chương, map 41 phases → chương | Tiếng Việt |
| [thesis-chapter-templates.md](thesis-chapter-templates.md) | Đoạn văn mẫu cho từng chương với chỗ trống `[ ]` | Tiếng Việt |
| [abstract.md](abstract.md) | Tóm tắt/Abstract dài-ngắn × Việt-Anh + lời cảm ơn, cam đoan | Song ngữ |
| [glossary.md](glossary.md) | Từ điển thuật ngữ Việt-Anh chia 8 nhóm | Song ngữ |

### Cơ sở lý thuyết và phương pháp

| File | Vai trò |
|---|---|
| [related-work.md](related-work.md) | 31 references chia 8 nhóm (Lakehouse, Kimball, Text-to-SQL, agents, guardrails…) |
| [evaluation-methodology.md](evaluation-methodology.md) | Phương pháp đánh giá chính thức: goals, metrics, reproduction |
| [production-roadmap.md](production-roadmap.md) | Hướng phát triển sau bảo vệ |

### Hình ảnh và bảo vệ

| File | Vai trò |
|---|---|
| [architecture-diagrams.md](architecture-diagrams.md) | 7 sơ đồ Mermaid cho Chương 3 |
| [figures-and-tables-index.md](figures-and-tables-index.md) | Danh mục 14-16 hình + 13-15 bảng + 6-8 đoạn mã |
| [defense-presentation.md](defense-presentation.md) | Outline 18 slide + 20 câu Q&A dự đoán |

---

## Map: thesis docs ↔ chương báo cáo

| Chương | Tài liệu hỗ trợ chính |
|---|---|
| Chương 1 — Giới thiệu | [thesis-outline.md](thesis-outline.md) §1, [abstract.md](abstract.md) |
| Chương 2 — Cơ sở lý thuyết | [related-work.md](related-work.md), [thesis-outline.md](thesis-outline.md) §2 |
| Chương 3 — Thiết kế hệ thống | [architecture-diagrams.md](architecture-diagrams.md), [thesis-chapter-templates.md](thesis-chapter-templates.md) §3 |
| Chương 4 — Triển khai | [thesis-chapter-templates.md](thesis-chapter-templates.md) §4, [figures-and-tables-index.md](figures-and-tables-index.md) |
| Chương 5 — Đánh giá | [evaluation-methodology.md](evaluation-methodology.md), [thesis-chapter-templates.md](thesis-chapter-templates.md) §5 |
| Chương 6 — Kết luận | [production-roadmap.md](production-roadmap.md), [thesis-chapter-templates.md](thesis-chapter-templates.md) §6 |

---

## Liên hệ với tài liệu hệ thống

Khi cần dẫn chứng cụ thể trong báo cáo, các tài liệu **kỹ thuật và vận hành**
nằm ở thư mục mẹ:

| Tài liệu | Đường dẫn |
|---|---|
| Roadmap 41 phases | [../development-roadmap.md](../development-roadmap.md) |
| Quyết định mô hình hóa | [../modeling-decisions.md](../modeling-decisions.md) |
| Hợp đồng dữ liệu Bronze | [../data-contracts.md](../data-contracts.md) |
| Star schema chi tiết | [../gold-star-schema.md](../gold-star-schema.md) |
| Kiến trúc | [../architecture.md](../architecture.md) |
| Runbook vận hành | [../runbook.md](../runbook.md) |
| Kết quả đánh giá agent | [../agent-evaluation-results.json](../agent-evaluation-results.json) |
| Báo cáo chất lượng dữ liệu | [../data-quality-report.md](../data-quality-report.md) |
| Báo cáo hiệu năng | [../performance-report.md](../performance-report.md) |
| 12 demo scenarios | [../demo-scenarios.md](../demo-scenarios.md) |
| Release checklist | [../release-checklist.md](../release-checklist.md) |

Quy ước trong toàn bộ thư mục `thesis/`:
- Đường dẫn `../something.md` = tài liệu trong `docs/`.
- Đường dẫn `../../something` = file ở repo root (vd: `AGENTS.md`, `services/`, `contracts/`).
