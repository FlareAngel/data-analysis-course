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
    orders={r['order_id'] for r in rows if r['row_type']=='ORDER' and r['order_date'][:4]=='2023' and r['region']=='NE' and r['state']=='SETTLED'}
    payments={r['payment_id']:r for r in rows if r['row_type']=='PAYMENT' and r['order_id'] in orders and r['state']=='SUCCESS'}
    refunds=[r for r in rows if r['row_type']=='REFUND' and r['state']=='SUCCESS' and r['parent_payment_id'] in payments]
    paid=sum((Decimal(p['amount']) for p in payments.values()),Decimal(0))
    ref=sum((Decimal(r['amount']) for r in refunds),Decimal(0))
    return {'settled_order_count':len(orders),'successful_payment_count':len(payments),'successful_refund_count':len(refunds),'gross_paid':money(paid),'refunded':money(ref),'net_received':money(paid-ref)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
