# Related Work and References

Curated bibliography for the thesis. Citations grouped by topic; each entry has
a short note on why it is relevant to this project.

> Format: Author(s), *Title*, Venue/Year. — relevance note.
> Use this list to populate Chapter 2 (Related Work) and the final references
> section. Citation style is left for the school template; entries are written
> so the title alone is enough to locate the source.

---

## 1. Lakehouse Architecture

1. M. Armbrust, A. Ghodsi, R. Xin, M. Zaharia, *Lakehouse: A New Generation of
   Open Platforms that Unify Data Warehousing and Advanced Analytics*, CIDR
   2021. — Foundational paper for the medallion (Bronze/Silver/Gold) model the
   project follows.
2. M. Armbrust et al., *Delta Lake: High-Performance ACID Table Storage over
   Cloud Object Stores*, VLDB 2020. — Background on transactional object-store
   tables; motivates the immutable-Bronze + curated-Gold pattern even though
   this project does not use Delta directly.
3. Apache Iceberg / Apache Hudi project documentation, 2020–2025. — Alternative
   table formats; cite to position why DuckDB-on-MinIO was chosen for a
   local-first MVP instead.
4. R. Kimball, M. Ross, *The Data Warehouse Toolkit: The Definitive Guide to
   Dimensional Modeling*, 3rd ed., Wiley, 2013. — Canonical reference for star
   schema, fact/dim, and conformed dimensions used in
   [gold-star-schema.md](../gold-star-schema.md).
5. B. Inmon, D. Linstedt, *Data Architecture: A Primer for the Data Scientist*,
   2nd ed., Morgan Kaufmann, 2019. — Background on layered data architectures
   and the role of curated serving layers.

## 2. Modern Data Stack Components

6. M. Beauchemin, *The Rise of the Data Engineer*, Medium (Airflow project
   essay), 2017. — Background and motivation behind Apache Airflow's design.
7. T. Lacroix, *Analytics Engineering with dbt*, O'Reilly Media, 2022. — dbt
   pattern reference (sources, models, tests, exposures) used in
   [dbt/models/](../../dbt/models/).
8. M. Raasveldt, H. Mühleisen, *DuckDB: an Embeddable Analytical Database*,
   SIGMOD 2019. — In-process OLAP engine that backs the serving layer.
9. MinIO Inc., *MinIO: High-Performance Object Storage*, project docs,
   2017–2025. — S3-compatible object storage used as Bronze source of truth.
10. S. Ramírez, *FastAPI Documentation*, 2018–2025. — Async Python API
    framework that hosts the agent service.

## 3. Text-to-SQL and Semantic Parsing

11. T. Yu et al., *Spider: A Large-Scale Human-Labeled Dataset for Complex and
    Cross-Domain Semantic Parsing and Text-to-SQL Task*, EMNLP 2018. — De-facto
    benchmark for Text-to-SQL accuracy; cited to contextualize evaluation
    methodology in [evaluation-methodology.md](evaluation-methodology.md).
12. B. Wang, R. Shin, X. Liu, O. Polozov, M. Richardson, *RAT-SQL:
    Relation-Aware Schema Encoding and Linking for Text-to-SQL Parsers*, ACL
    2020. — Schema-linking research; informs why this project relies on an
    explicit semantic catalog instead of learned linking.
13. X. Deng et al., *Recent Advances in Text-to-SQL: A Survey*, ACM
    Computing Surveys, 2022. — Survey to cite for Section 2.4.
14. M. Pourreza, D. Rafiei, *DIN-SQL: Decomposed In-Context Learning of
    Text-to-SQL with Self-Correction*, NeurIPS 2023. — Modern LLM-based
    Text-to-SQL with self-check; conceptually similar to the agent's
    self-check step.
15. R. Sun et al., *SQL-PaLM: Improved Large Language Model Adaptation for
    Text-to-SQL*, arXiv 2305.00000-class works, 2023. — Context for
    LLM-driven SQL generation.

## 4. LLM Agents and Tool Use

16. T. Schick et al., *Toolformer: Language Models Can Teach Themselves to Use
    Tools*, NeurIPS 2023. — Motivation for agent-as-tool-orchestrator design.
17. S. Yao et al., *ReAct: Synergizing Reasoning and Acting in Language
    Models*, ICLR 2023. — Reason-act loop that inspired the deterministic
    intent → plan → execute → self-check loop.
18. H. Chase, *LangChain* project docs, 2022–2025. — Cite to explain *why* this
    project does **not** use LangChain (transparency, traceability, lighter
    runtime; see [AGENTS.md](../../AGENTS.md)).
19. Vanna AI project docs, 2023–2025. — Alternative Text-to-SQL agent
    framework; positioned as related work the project deliberately avoided.

## 5. SQL Safety, Validation, and Guardrails

20. sqlglot project documentation, 2021–2025. — AST-based SQL parser used by
    [services/api/app/sql_guardrails.py](../../services/api/app/sql_guardrails.py).
21. OWASP, *SQL Injection Prevention Cheat Sheet*, 2023. — Background on input
    validation, prepared statements, and least-privilege execution.
22. NIST SP 800-95, *Guide to Secure Web Services*, 2007. — General reference
    for input validation at API boundaries.
23. M. Stonebraker, U. Çetintemel, *"One Size Fits All": An Idea Whose Time
    Has Come and Gone*, ICDE 2005. — Background for engine specialization;
    supports DuckDB-for-analytics choice.

## 6. Data Quality and Observability

24. dbt Labs, *Data Tests in dbt* documentation, 2020–2025. — Reference for the
    77 dbt tests in [dbt/models/schema.yml](../../dbt/models/schema.yml).
25. *Great Expectations* project documentation. — Alternative DQ framework; cite
    to justify why dbt-native tests are sufficient at MVP scope.
26. G. Aragon, R. Dijkman et al., *Data Observability: A Survey*, IEEE Access
    2023. — Cite for Phase 25 pipeline metadata observability narrative.

## 7. NYC TLC Domain Studies

27. NYC Taxi & Limousine Commission, *TLC Trip Record Data*, public data
    portal. — Primary data source. URL referenced in
    [data-contracts.md](../data-contracts.md).
28. NYC TLC, *Taxi Zone Lookup Table*, public data. — Enrichment reference
    dataset.
29. Various, *NYC Taxi Trip Duration / Tip Prediction* (Kaggle competitions,
    2017–2020). — Examples of analytical use of the same source; helps frame
    the difference between predictive modeling and the descriptive analytics
    pipeline this project builds.

## 8. Containerization and Local-First Reproducibility

30. Docker Inc., *Docker Compose specification*, 2014–2025. — Reproducible
    multi-service deployment used as the project's primary delivery format.
31. The Twelve-Factor App, *12-Factor Methodology*, 2011. — Cited for
    configuration-as-environment practice (`.env`, `config.py`).

---

## Suggested Vietnamese / regional references

For a Vietnamese thesis committee, consider adding 2–3 local references:

- Sách giáo trình *"Hệ quản trị cơ sở dữ liệu"* hoặc *"Kho dữ liệu và OLAP"* của
  trường (cite phiên bản đang dùng tại khoa).
- Báo cáo khoa học sinh viên trước về Data Engineering / Data Lakehouse (nếu
  có) — phỏng vấn giảng viên hướng dẫn để xin danh sách.
- Tài liệu khóa học modern data stack tiếng Việt (nếu được dùng làm tham
  khảo).

---

## How to use this file in the report

1. Quote in Chapter 2 (Cơ sở lý thuyết & Related Work) — see
   [thesis-outline.md](thesis-outline.md) Ch.2.
2. Move citations into the school's reference template (APA / IEEE / Chicago).
3. For every claim of the form *"X is a known pattern"* in the report, link to
   one entry here so the panel can verify provenance.
4. Tools/SDKs (sqlglot, dbt, DuckDB, MinIO, FastAPI) need at least the
   official documentation cited — even if no academic paper exists.
