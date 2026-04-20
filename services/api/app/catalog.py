from pathlib import Path

import yaml

from app.models import SchemaField, SchemaResponse, SchemaTable


def load_schema_catalog(path: Path) -> SchemaResponse:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    tables = []
    for item in payload.get("tables", []):
        fields = [
            SchemaField(name=field["name"], description=field.get("description", ""))
            for field in item.get("fields", [])
        ]
        tables.append(
            SchemaTable(
                name=item["name"],
                description=item.get("description", ""),
                fields=fields,
            )
        )
    return SchemaResponse(tables=tables)
