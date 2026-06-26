"""Execution-accuracy scoring for Spider/BIRD predictions on SQLite.

Execution accuracy = does the predicted SQL return the same result set as the gold
SQL when run on the same database. This is the primary text-to-SQL metric reported
by published systems, so our numbers line up beside theirs.

Comparison rule (matches the common Spider convention):
- If the gold query has ORDER BY, row order is significant -> compare ordered lists.
- Otherwise the result is a multiset -> compare with collections.Counter
  (order-insensitive, duplicate-sensitive, no fragile cross-type sorting).

For comparability with published leaderboard numbers, also run the official Spider
test-suite evaluator (see README.md); this module is the lightweight in-repo scorer.
"""

from __future__ import annotations

import re
import sqlite3
from collections import Counter

_ORDER_BY = re.compile(r"\border\s+by\b", re.IGNORECASE)


def execute_on_sqlite(db_path: str, sql: str, timeout: float = 30.0):
    """Run one SQL statement read-only. Returns (rows, error_message)."""
    con = sqlite3.connect(db_path, timeout=timeout)
    con.text_factory = lambda b: b.decode("utf-8", errors="replace")
    try:
        rows = con.execute(sql).fetchall()
        return [tuple(row) for row in rows], None
    except Exception as exc:  # noqa: BLE001 - benchmark records any execution failure
        return None, str(exc)
    finally:
        con.close()


def order_matters(gold_sql: str) -> bool:
    return bool(_ORDER_BY.search(gold_sql))


def result_sets_match(pred_rows, gold_rows, *, ordered: bool) -> bool:
    if pred_rows is None or gold_rows is None:
        return False
    if ordered:
        return pred_rows == gold_rows
    return Counter(pred_rows) == Counter(gold_rows)


def score_prediction(db_path: str, pred_sql: str, gold_sql: str) -> dict:
    """Compare one prediction against gold. Returns a per-example result dict."""
    gold_rows, gold_err = execute_on_sqlite(db_path, gold_sql)
    if gold_err is not None:
        return {"correct": False, "valid": False, "gold_error": gold_err, "exec_error": None}

    pred_rows, pred_err = execute_on_sqlite(db_path, pred_sql)
    valid = pred_err is None
    correct = valid and result_sets_match(pred_rows, gold_rows, ordered=order_matters(gold_sql))
    return {"correct": correct, "valid": valid, "gold_error": None, "exec_error": pred_err}


def _self_test() -> None:
    import os
    import tempfile

    tmp = tempfile.mkdtemp()
    db_path = os.path.join(tmp, "t.sqlite")
    con = sqlite3.connect(db_path)
    con.executescript(
        """
        CREATE TABLE singer (singer_id INTEGER, name TEXT, country TEXT);
        INSERT INTO singer VALUES (1,'A','US'),(2,'B','UK'),(3,'C','US');
        """
    )
    con.commit()
    con.close()

    gold = "SELECT country, COUNT(*) FROM singer GROUP BY country"
    same = "SELECT country, COUNT(*) FROM singer GROUP BY country"
    reordered_cols = "SELECT COUNT(*), country FROM singer GROUP BY country"  # different column order
    wrong = "SELECT country FROM singer"
    broken = "SELECT nope FROM singer"

    assert score_prediction(db_path, same, gold)["correct"] is True
    assert score_prediction(db_path, reordered_cols, gold)["correct"] is False
    assert score_prediction(db_path, wrong, gold)["correct"] is False
    r = score_prediction(db_path, broken, gold)
    assert r["correct"] is False and r["valid"] is False

    # ORDER BY sensitivity.
    gold_ord = "SELECT name FROM singer ORDER BY name ASC"
    desc = "SELECT name FROM singer ORDER BY name DESC"
    assert score_prediction(db_path, gold_ord, gold_ord)["correct"] is True
    assert score_prediction(db_path, desc, gold_ord)["correct"] is False

    print("scorer self-test OK")


if __name__ == "__main__":
    _self_test()
