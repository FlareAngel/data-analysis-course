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

def event(r,wrong=False):
    n=int(r['event_epoch']);is_ms=r['unit'] in ('ms','millis')
    # 典型错误是把秒时间戳也当成毫秒；不会溢出 datetime 范围
    return datetime.fromtimestamp(n/1000 if (is_ms or wrong) else n,tz=timezone.utc)
def solve(data,variant=False):
    lo=dt('2024-02-01T00:00:00+00:00');hi=dt('2024-03-01T00:00:00+00:00')
    chosen=[r for r in data if lo<=event(r,variant)<hi and r['region'] in ('NE','N-E') and r['status'] in ('PAID','P','DONE')]
    return {'payment_count':len(chosen),'total_yuan':cents(sum((money(r['amount_yuan']) for r in chosen),Decimal(0)))}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
