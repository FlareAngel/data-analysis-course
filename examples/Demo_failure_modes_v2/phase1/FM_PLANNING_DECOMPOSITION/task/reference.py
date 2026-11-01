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
         if not (r['event_time'][:4]=='2023' and r['region']=='NE'): continue
         key=(r['event_time'],int(r['seq']),r['event_id'])
         if r['account_id'] not in latest or key>latest[r['account_id']][0]: latest[r['account_id']]=(key,r)
        return sum(r['state']=='ACTIVE' and r['kyc']=='KYC_OK' and int(r['score'])>=80 for _,r in latest.values())
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
