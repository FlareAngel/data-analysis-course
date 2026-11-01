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
    lo=dt('2024-07-01T00:00:00+00:00');hi=dt('2024-07-04T00:00:00+00:00')
    intervals=[]
    for r in data:
        if r['region'] not in ('NE','N-E') or r['service'] not in ('API','api') or r['category'] not in ('OUTAGE','DOWN'):continue
        a,b=dt(r['start_at']),dt(r['end_at'])
        if b<=lo or a>=hi:continue
        intervals.append((a if variant else max(lo,a),b if variant else min(hi,b)))
    intervals.sort();merged=[]
    for a,b in intervals:
        if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else:merged.append((a,b))
    minutes=int(sum((b-a).total_seconds() for a,b in merged)/60)
    base=int((hi-lo).total_seconds()/60)
    return {'downtime_minutes':minutes,'availability_percent':cents(Decimal(base-minutes)*100/Decimal(base))}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
