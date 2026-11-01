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
    cutoff=dt('2024-11-01T00:00:00+00:00');lookback=dt('2024-10-02T00:00:00+00:00');groups=defaultdict(list)
    for r in data:
        if r['region'] in ('NE','N-E') and dt(r['occurred_at'])<cutoff:groups[r['member_id']].append(r)
    ids=[]
    for k,rr in groups.items():
        selected=[r for r in rr if r['member_state'] in ('ACTIVE','ENABLED')] if variant else rr
        if not selected:continue
        latest=max(selected,key=lambda r:(dt(r['occurred_at']),int(r['seq'])))
        if latest['member_state'] not in ('ACTIVE','ENABLED'):continue
        if any(lookback<=dt(r['occurred_at'])<cutoff and r['action'] in ('LOGIN','SIGNIN') for r in rr):ids.append(k)
    ids.sort()
    return {'member_ids':ids,'member_count':len(ids)}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
