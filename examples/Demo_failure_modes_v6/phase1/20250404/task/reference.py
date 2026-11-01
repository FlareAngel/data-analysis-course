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
    lo=dt('2024-04-01T00:00:00+00:00');hi=dt('2024-04-06T00:00:00+00:00')
    xs=[r for r in data if lo<=dt(r['delivered_at'])<hi and r['region'] in ('NE','N-E') and r['status'] in ('DELIVERED','DONE','D')]
    xs.sort(key=lambda r:(r['delivered_at'] if variant else dt(r['delivered_at']),r['order_id']))
    return {'order_ids':[r['order_id'] for r in xs[:5]],'first_delivery_utc':dt(xs[0]['delivered_at']).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if xs else ''}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
