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
    lo=dt('2024-12-01T00:00:00+00:00');hi=dt('2025-01-01T00:00:00+00:00')
    heads=[r for r in data if r['entity']=='HEADER' and r['region'] in ('NE','N-E') and r['status']=='OPEN' and lo<=dt(r['posted_at'])<=(hi if variant else hi-timedelta(microseconds=1))]
    passed=[];failed=[]
    for h in heads:
        latest={}
        for r in data:
            if r['invoice_id']!=h['invoice_id'] or r['entity'] not in ('LINE','ITEM'):continue
            if not variant and dt(r['received_at'])>=hi:continue
            key=r['line_id'];rank=(int(r['revision']),dt(r['received_at']))
            if key not in latest or rank>latest[key][0]:latest[key]=(rank,r)
        amt=sum((money(r['amount']) for rank,r in latest.values() if r['status']=='POSTED'),Decimal(0))
        (passed if latest and amt==money(h['amount']) else failed).append(h['invoice_id'])
    return {'passed_ids':sorted(passed),'failed_ids':sorted(failed),'checked_count':len(heads)}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
