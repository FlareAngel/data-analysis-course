import csv, json
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
from zoneinfo import ZoneInfo

def records():
    with (Path(__file__).parent/'data.csv').open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def dt(x):
    return datetime.fromisoformat(x.replace('Z','+00:00'))

def money(x):
    return Decimal(x or '0')

def cents(x):
    return str(Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

def solve(data,variant=False):
    lo=dt('2024-05-01T00:00:00+00:00');hi=dt('2024-06-01T00:00:00+00:00')
    orders={r['order_id'] for r in data if r['entity_type']=='ORDER' and r['region'] in ('NE','N-E')}
    payments={r['entity_id']:r for r in data if r['entity_type'] in ('PAYMENT','PAY','CAPTURE') and r['order_id'] in orders and lo<=dt(r['event_at'])<hi and r['region'] in ('NE','N-E') and r['state']=='OK'}
    amt=sum((money(r['amount']) for r in payments.values()),Decimal(0))
    for r in data:
        if r['entity_type'] in ('REFUND','REVERSAL') and r['parent_payment_id'] in payments and r['state']=='POSTED' and (variant or lo<=dt(r['event_at'])<hi):amt-=money(r['amount'])
    return {'paid_count':len(payments),'net_receipts':cents(amt)}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
