"""Lowercase unquoted SQL identifiers so guardrail name-matching is case-fair.

SQLite is case-insensitive; Spider gold and the LLM mix cases. We lowercase identifiers
(not string literals) on the SQL side to match the lowercased benchmark catalog. Needs
sqlglot, so this runs only inside the `api` image.
"""

from __future__ import annotations

import sqlglot
from sqlglot.optimizer.normalize_identifiers import normalize_identifiers


def to_lower_identifiers(sql: str, *, read: str = "sqlite") -> str:
    """Return the SQL with unquoted identifiers lowercased. Falls back to input on failure."""
    try:
        expression = sqlglot.parse_one(sql, read=read)
        return normalize_identifiers(expression, dialect=read).sql(dialect="duckdb")
    except Exception:  # noqa: BLE001 - if it cannot parse, let the guardrail report the real error
        return sql
