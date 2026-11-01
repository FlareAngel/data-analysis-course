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
    lo=dt('2024-02-29T00:00:00+00:00');hi=dt('2024-03-01T00:00:00+00:00')
    v=[money(r['amount_yuan']) for r in data if r['region'] in ('NE','N-E') and r['status'] in ('Y','OK') and lo<=dt(r['posted_at'])<=(hi if variant else hi-timedelta(microseconds=1))]
    invalid=sum(x<=0 for x in v);abnormal=sum(x>5000 for x in v)
    ok=[x for x in v if x>0 and (x<=5000)]
    return {'invalid_count':invalid,'abnormal_count':abnormal,'valid_count':len(ok),'valid_amount':cents(sum(ok,Decimal(0)))}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
