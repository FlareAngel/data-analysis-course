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
        tz=ZoneInfo('America/New_York')
        count=0
        for r in records:
         if not(r['region']=='NE' and r['event_type']=='PAYMENT_CAPTURED' and r['channel'] in {'WEB','APP'}): continue
         local=datetime.fromisoformat(r['event_time'].replace('Z','+00:00')).astimezone(tz)
         if local.date().isoformat()=='2024-11-03' and 1<=local.hour<2: count+=1
        return count
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
