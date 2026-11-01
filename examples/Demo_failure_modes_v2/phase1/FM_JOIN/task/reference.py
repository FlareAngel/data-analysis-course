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
        orders={r['order_id'] for r in records if r['row_type']=='ORDER' and r['order_date'][:4]=='2023' and r['region']=='NE' and r['state']=='SETTLED'}
        valid_pay={r['payment_id']:Decimal(r['amount']) for r in records if r['row_type']=='PAYMENT' and r['order_id'] in orders and r['state']=='SUCCESS'}
        total=sum(valid_pay.values(),Decimal('0'))-sum((Decimal(r['amount']) for r in records if r['row_type']=='REFUND' and r['state']=='SUCCESS' and r['parent_payment_id'] in valid_pay),Decimal('0'))
        return float(total.quantize(Decimal('.01')))
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
