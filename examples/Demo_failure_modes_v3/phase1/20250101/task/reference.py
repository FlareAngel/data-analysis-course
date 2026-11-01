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
    selected=[r for r in rows if '2023-01-01'<=r['order_date']<'2024-01-01' and r['region']=='NE' and r['channel'] in ('WEB','APP') and r['status']=='SETTLED']
    net=sum((Decimal(r['gross_amount'])-Decimal(r['refund_amount']) for r in selected),Decimal(0))
    return {'region':'东北','channels':['APP','WEB'],'order_count':len(selected),'net_amount':money(net)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
