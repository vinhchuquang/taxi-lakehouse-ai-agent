#!/bin/sh
# ponytail: ephemeral deps for the vendored Spider test-suite evaluator (nltk + func_timeout).
# Runs inside a --rm container only; does not touch the persistent image or host Python.
set -e
pip install -q nltk func_timeout sqlparse
python - <<'PY'
import nltk
for pkg in ("punkt", "punkt_tab"):
    try:
        nltk.download(pkg, quiet=True)
    except Exception as e:
        print("nltk download skip", pkg, e)
PY
python benchmarks/spider/test-suite-sql-eval/evaluation.py \
  --gold benchmarks/spider/gold_dev.txt \
  --pred benchmarks/spider/results_full.pred_wrapped.sql \
  --db spider_data/spider_data/database \
  --table spider_data/spider_data/tables.json \
  --etype exec
