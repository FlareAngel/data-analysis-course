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

def ver(s):
    return int(s.removeprefix('ver:').removeprefix('rev').removeprefix('v'))
def solve(data,variant=False):
    cutoff=dt('2024-10-01T00:00:00+00:00');latest={}
    for r in data:
        if r['region'] not in ('NE','N-E'):continue
        if not variant and dt(r['ingested_at'])>=cutoff:continue
        k=r['record_id'];key=(ver(r['version']),dt(r['updated_at']))
        if k not in latest or key>latest[k][0]:latest[k]=(key,r)
    ids=sorted(k for k,(_,r) in latest.items() if r['status'] in ('DONE','COMPLETE'))
    return {'completed_ids':ids,'completed_count':len(ids),'completed_amount':cents(sum((money(latest[k][1]['amount']) for k in ids),Decimal(0)))}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
