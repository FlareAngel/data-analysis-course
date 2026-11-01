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
    end=dt('2024-03-01T00:00:00+00:00');latest={}
    for r in data:
        if r['region'] not in ('NE','N-E'):continue
        if dt(r['event_at' if not variant else 'opened_at'])>=end:continue
        k=r['ticket_id'];rank=(dt(r['event_at']),int(r['event_seq']))
        if k not in latest or rank>latest[k][0]:latest[k]=(rank,r)
    ids=sorted(k for k,(v,r) in latest.items() if r['status'] in ('CLOSED','DONE'))
    return {'closed_ticket_count':len(ids),'closed_ticket_ids':ids}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
