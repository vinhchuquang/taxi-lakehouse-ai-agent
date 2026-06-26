"""Adapt a Spider/BIRD `tables.json` database schema into the agent's SchemaResponse.

This is the keystone that lets the existing read-only wrapper
(`generate_sql_with_openai` + `validate_gold_select`) run on benchmark databases
instead of only the taxi Gold surface.

Decisions made here, and why (see benchmarks/spider/README.md):
- Every benchmark table is marked `execution_enabled=True` so the guardrail does
  not reject it as "cataloged but not execution-enabled".
- Every table uses `table_type="aggregate_mart"` so the guardrail allows `SELECT *`,
  which Spider/BIRD gold queries use heavily (otherwise valid queries fail unfairly).
- `allowed_joins` are generated from the benchmark's declared foreign keys — the
  principled analog of the taxi catalog's curated join paths.
- All columns go into `fields`; the guardrail unions fields/dimensions/metrics for
  column validation, so this is sufficient.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.models import (  # noqa: E402
    SchemaField,
    SchemaForeignKey,
    SchemaJoin,
    SchemaResponse,
    SchemaTable,
)


def build_schema_response(db_schema: dict) -> SchemaResponse:
    """Convert one Spider `tables.json` entry into a SchemaResponse."""
    # SQLite identifiers are case-insensitive, but Spider mixes cases between schema and
    # queries. Lowercase every name so the guardrail's exact-match comparison is fair;
    # SQL identifiers are lowercased symmetrically in sqlnorm.to_lower_identifiers.
    table_names = [name.lower() for name in db_schema["table_names_original"]]
    columns = [[idx, str(name).lower()] for idx, name in db_schema["column_names_original"]]
    primary_keys = set(db_schema.get("primary_keys", []))
    foreign_keys = db_schema.get("foreign_keys", [])

    # Per-table column names (skip the synthetic "*" at column index 0).
    table_columns: dict[int, list[str]] = {idx: [] for idx in range(len(table_names))}
    for col_idx, (table_idx, col_name) in enumerate(columns):
        if table_idx < 0:
            continue
        table_columns[table_idx].append(col_name)

    # Per-table primary keys.
    table_primary_keys: dict[int, list[str]] = {idx: [] for idx in range(len(table_names))}
    for col_idx in primary_keys:
        table_idx, col_name = columns[col_idx]
        if table_idx >= 0:
            table_primary_keys[table_idx].append(col_name)

    # Foreign keys -> per-table SchemaForeignKey + global SchemaJoin list.
    table_foreign_keys: dict[int, list[SchemaForeignKey]] = {idx: [] for idx in range(len(table_names))}
    table_joins: dict[int, list[SchemaJoin]] = {idx: [] for idx in range(len(table_names))}
    for source_col_idx, target_col_idx in foreign_keys:
        src_table_idx, src_col = columns[source_col_idx]
        tgt_table_idx, tgt_col = columns[target_col_idx]
        if src_table_idx < 0 or tgt_table_idx < 0:
            continue
        table_foreign_keys[src_table_idx].append(
            SchemaForeignKey(
                column=src_col,
                references_table=table_names[tgt_table_idx],
                references_column=tgt_col,
            )
        )
        table_joins[src_table_idx].append(
            SchemaJoin(
                left_table=table_names[src_table_idx],
                left_column=src_col,
                right_table=table_names[tgt_table_idx],
                right_column=tgt_col,
            )
        )

    tables = [
        SchemaTable(
            name=name,
            description="",
            table_type="aggregate_mart",
            execution_enabled=True,
            grain="",
            fields=[SchemaField(name=col, description="") for col in table_columns[idx]],
            dimensions=[],
            metrics=[],
            allowed_filters=[],
            primary_key=table_primary_keys[idx],
            foreign_keys=table_foreign_keys[idx],
            allowed_joins=table_joins[idx],
            preferred_questions=[],
        )
        for idx, name in enumerate(table_names)
    ]
    return SchemaResponse(tables=tables)


def load_spider_schemas(tables_json_path: str | Path) -> dict[str, SchemaResponse]:
    """Load every database schema from a Spider/BIRD `tables.json`, keyed by db_id."""
    payload = json.loads(Path(tables_json_path).read_text(encoding="utf-8"))
    return {entry["db_id"]: build_schema_response(entry) for entry in payload}


_SAMPLE_SCHEMA = {
    "db_id": "concert_singer",
    "table_names_original": ["stadium", "singer", "concert"],
    "column_names_original": [
        [-1, "*"],
        [0, "stadium_id"],
        [0, "name"],
        [0, "capacity"],
        [1, "singer_id"],
        [1, "name"],
        [1, "country"],
        [2, "concert_id"],
        [2, "stadium_id"],
        [2, "year"],
    ],
    "column_types": ["text", "number", "text", "number", "number", "text", "text", "number", "number", "text"],
    "primary_keys": [1, 4, 7],
    "foreign_keys": [[8, 1]],
}


if __name__ == "__main__":
    schema = build_schema_response(_SAMPLE_SCHEMA)
    assert {t.name for t in schema.tables} == {"stadium", "singer", "concert"}
    concert = next(t for t in schema.tables if t.name == "concert")
    assert [f.name for f in concert.fields] == ["concert_id", "stadium_id", "year"]
    assert concert.foreign_keys[0].references_table == "stadium"
    assert concert.allowed_joins[0].left_table == "concert"
    assert concert.allowed_joins[0].right_table == "stadium"
    stadium = next(t for t in schema.tables if t.name == "stadium")
    assert stadium.primary_key == ["stadium_id"]
    print("schema_adapter self-test OK:", len(schema.tables), "tables,",
          sum(len(t.allowed_joins) for t in schema.tables), "join paths")
