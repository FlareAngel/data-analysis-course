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
        eligible=[r for r in records if r['created_at'][:4]=='2023' and r['region']=='NE' and r['status']=='PAID' and r['channel'] in {'WEB','APP'}]
        eligible.sort(key=lambda r:(-Decimal(r['amount']),r['created_at'],r['invoice_id']))
        return eligible[6]['invoice_id']
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
