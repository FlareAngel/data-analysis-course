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

def solve(data, variant=False):
    lo=dt('2024-01-01T00:00:00+00:00');hi=dt('2024-04-01T00:00:00+00:00')
    items=[r for r in data if lo<=dt(r['created_at' if variant else 'confirmed_at']).astimezone(timezone.utc)<hi and r['region'] in ('NE','N-E') and r['state'] in ('C','SETTLED','OK') and r['channel'] in ('APP','WEB','online')]
    return {'order_count':len(items),'total_amount':cents(sum((money(r['amount']) for r in items),Decimal('0')))}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
