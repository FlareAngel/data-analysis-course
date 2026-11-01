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
        line_sums=defaultdict(lambda:Decimal('0')); line_counts=Counter()
        for r in records:
         if r['row_type']=='LINE':
          line_sums[r['invoice_id']]+=Decimal(r['line_amount']); line_counts[r['invoice_id']]+=1
        return sum(r['row_type']=='HEADER' and r['invoice_date'][:4]=='2023' and r['region']=='NE' and r['state']=='POSTED' and line_counts[r['invoice_id']]>0 and line_sums[r['invoice_id']]==Decimal(r['declared_total']) for r in records)
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
