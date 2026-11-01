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
    tz=ZoneInfo('America/Los_Angeles');day=date(2024,11,3)
    chosen=[]
    for r in data:
        if r['region'] not in ('NE','N-E') or r['event_type'] not in ('CAPTURE','CAPTURE_OK','C'):continue
        t=dt(r['occurred_at']);loc=t.astimezone(timezone(timedelta(hours=-7)) if variant else tz)
        if loc.date()==day:chosen.append(loc)
    return {'local_day_count':len(chosen),'hour_01_pdt':sum(t.hour==1 and t.utcoffset()==timedelta(hours=-7) for t in chosen),'hour_01_pst':sum(t.hour==1 and t.utcoffset()==timedelta(hours=-8) for t in chosen)}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
