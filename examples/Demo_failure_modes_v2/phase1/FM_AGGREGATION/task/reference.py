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
        rows=[r for r in records if r['sale_date'][:4]=='2023' and r['region']=='NE' and r['channel'] in {'WEB','APP'} and r['state']=='PAID']
        num=sum((Decimal(r['discount_amount']) for r in rows),Decimal('0'))
        den=sum((Decimal(r['qty'])*Decimal(r['unit_list_price']) for r in rows),Decimal('0'))
        return float((Decimal('100')*num/den).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
    return {"answer": _calculate(records)}

if __name__ == '__main__':
    import pandas as pd
    path = Path(__file__).resolve().parent / 'data.csv'
    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(json.dumps(reference(data), ensure_ascii=False))
