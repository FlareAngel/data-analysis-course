from __future__ import annotations
import csv
import json
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter, defaultdict
from typing import Any

def reference(df) -> dict[str,Any]:
    """Receives a pandas DataFrame; returns the standard answer as a JSON-compatible dict."""
    records = df.fillna('').astype(str).to_dict(orient='records')
    def _calculate(records):
        total=sum(((Decimal(r['taxable_amount'])*Decimal(r['tax_rate'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP) for r in records if r['effective_date'][:4]=='2023' and r['region']=='NE' and r['state']=='POSTED'),Decimal('0'))
        return float(total.quantize(Decimal('.01')))
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
