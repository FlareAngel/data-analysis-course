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
        qualified_orders=set()
        for r in records:
         if r['order_date'][:4]=='2023' and r['region']=='NE' and r['status']=='PAID' and r['sku']=='KIT' and int(r['qty'])>=2:
          qualified_orders.add((r['customer_id'],r['order_id']))
        counts=Counter(customer for customer,_ in qualified_orders)
        return sum(n>=2 for n in counts.values())
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
