from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from app.models import QueryRequest, QueryResponse


def write_query_audit(
    *,
    path: str,
    request: QueryRequest,
    status: str,
    response: QueryResponse | None = None,
    error_type: str | None = None,
    error_detail: str | None = None,
) -> None:
    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "status": status,
        "question": request.question,
        "has_sql_override": request.sql is not None,
        "requested_max_rows": request.max_rows,
        "sql": response.sql if response else request.sql,
        "execution_ms": response.execution_ms if response else None,
        "warnings": response.warnings if response else [],
        "confidence": response.confidence if response else None,
        "requires_clarification": response.requires_clarification if response else False,
        "clarification_question": response.clarification_question if response else None,
        "agent_step_statuses": [
            {"name": step.name, "status": step.status} for step in response.agent_steps
        ]
        if response
        else [],
        "error_type": error_type,
        "error_detail": error_detail,
    }
    _append_jsonl(path, event)


def _append_jsonl(path: str, event: dict[str, Any]) -> None:
    try:
        audit_path = Path(path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=True, default=str))
            handle.write("\n")
    except OSError:
        # Audit logging must not make a read-only query fail.
        return
