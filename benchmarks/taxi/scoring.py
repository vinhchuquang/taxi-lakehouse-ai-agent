"""Pure scoring helpers for the taxi domain benchmark — stdlib only, no app deps, so the
runner and an offline re-scorer share identical logic (re-score saved rows without Docker).

Numbers compare by relative tolerance (math.isclose), not round-then-equal: a SUM computed
in a different order (float non-associativity) differs only past ~12 significant figures,
which tolerance absorbs, while round-then-equal wrongly splits values that straddle a
rounding boundary (e.g. ...29.95)."""

import math
import re
from decimal import Decimal
from itertools import permutations

_ORDER_BY = re.compile(r"\border\s+by\b", re.IGNORECASE)
_LIMIT = re.compile(r"\blimit\b", re.IGNORECASE)

_REL_TOL = 1e-6
_ABS_TOL = 1e-6


def is_ordered(gold_sql: str) -> bool:
    """Row order is semantic only for a ranking query (ORDER BY + LIMIT); a bare ORDER BY
    is cosmetic and compared as an unordered multiset."""
    return bool(_ORDER_BY.search(gold_sql) and _LIMIT.search(gold_sql))


def _as_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float, Decimal)):
        return float(value)
    return None


def _cell_close(a, b):
    na, nb = _as_number(a), _as_number(b)
    if na is not None and nb is not None:
        return math.isclose(na, nb, rel_tol=_REL_TOL, abs_tol=_ABS_TOL)
    return a == b


def _row_close(t1, t2):
    return len(t1) == len(t2) and all(_cell_close(a, b) for a, b in zip(t1, t2))


def _multiset_close(agent_proj, gold_proj):
    remaining = list(gold_proj)
    for tup in agent_proj:
        for i, other in enumerate(remaining):
            if _row_close(tup, other):
                remaining.pop(i)
                break
        else:
            return False
    return True


def values_match(agent_rows, agent_cols, gold_rows, gold_cols, ordered):
    """Execution-accuracy match that ignores column NAMES (like Spider): the agent is
    correct if some selection of its columns reproduces the gold value tuples. Tolerant of
    extra columns and renamed aliases; strict on row count/values and (when the gold query
    is a ranking with LIMIT) on order."""
    if len(agent_rows) != len(gold_rows):
        return False
    g = len(gold_cols)
    if len(agent_cols) > 8:  # ponytail: cap permutation blowup; real queries select few cols
        if not set(gold_cols).issubset(set(agent_cols)):
            return False
        agent_cols = list(gold_cols)
    gold_proj = [tuple(r.get(c) for c in gold_cols) for r in gold_rows]
    agent_full = [[r.get(c) for c in agent_cols] for r in agent_rows]
    for combo in permutations(range(len(agent_cols)), g):
        agent_proj = [tuple(row[i] for i in combo) for row in agent_full]
        if ordered:
            if all(_row_close(a, b) for a, b in zip(agent_proj, gold_proj)):
                return True
        elif _multiset_close(agent_proj, gold_proj):
            return True
    return False
