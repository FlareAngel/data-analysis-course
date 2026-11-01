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
        latest={}
        for r in records:
         key=(r['received_at'],int(r['version']),r['raw_id'])
         if r['event_id'] not in latest or key>latest[r['event_id']][0]: latest[r['event_id']]=(key,r)
        orders={r['order_id'] for _,r in latest.values() if r['event_date'][:4]=='2023' and r['region']=='NE' and r['state']=='DELIVERED'}
        return len(orders)
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
