from __future__ import annotations
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter, defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

TWO = Decimal('0.01')
def money(value):
    return format(Decimal(value).quantize(TWO, rounding=ROUND_HALF_UP), '.2f')

def reference(df=None):
    """Returns {'answer': JSON value}. Optional pandas DataFrame accepted."""
    if df is None:
        with open(Path(__file__).with_name('data.csv'), encoding='utf-8-sig', newline='') as handle:
            rows=list(csv.DictReader(handle))
    else:
        rows=df.fillna('').astype(str).to_dict(orient='records')
    return {'answer': solve(rows)}



def solve(rows):
    eligible=[r for r in rows if r['sale_date'][:4]=='2023' and r['region']=='NE' and r['channel'] in ('WEB','APP') and r['state']=='PAID']
    basis=sum((Decimal(r['qty'])*Decimal(r['unit_list_price']) for r in eligible),Decimal(0))
    discount=sum((Decimal(r['discount_amount']) for r in eligible),Decimal(0))
    if basis==0: raise ValueError('zero denominator')
    rate=(Decimal(100)*discount/basis).quantize(TWO,rounding=ROUND_HALF_UP)
    return {'basis_amount':money(basis),'discount_amount':money(discount),'discount_rate_pct':float(rate)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
