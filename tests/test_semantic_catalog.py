from pathlib import Path

import yaml


def test_semantic_catalog_has_tables() -> None:
    catalog_path = Path("contracts/semantic_catalog.yaml")
    payload = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))

    assert "tables" in payload
    assert payload["tables"]
