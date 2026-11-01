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

import re
def solve(data,variant=False):
    lo=dt('2024-05-01T00:00:00+00:00');hi=dt('2024-06-01T00:00:00+00:00');eligible=[]
    for r in data:
        if r['region'] not in ('NE','N-E') or r['status'] not in ('CONFIRMED','YES','FINAL'):continue
        t=dt(r['effective_at'])
        if variant:
            match=re.search(r'2024-\d{2}-\d{2}',r['note'])
            if match:t=dt(match.group()+'T00:00:00+00:00')
        if lo<=t<hi:eligible.append(r)
    return {'approved_count':len(eligible),'approved_amount':cents(sum((money(r['amount']) for r in eligible),Decimal(0)))}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
