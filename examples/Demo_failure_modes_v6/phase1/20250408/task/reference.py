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
    cutoff=dt('2024-09-01T00:00:00+00:00');missing={'NA','N/A','null','NULL','--',''}
    recent={};n=0
    for r in data:
        if r['region'] not in ('NE','N-E') or (dt(r['observed_at'])>cutoff if variant else dt(r['observed_at'])>=cutoff):continue
        s=r['score_text'].strip()
        if s in missing:
            n+=1;continue
        k=r['account_id'];rank=(dt(r['observed_at']),int(r['revision']))
        if k not in recent or rank>recent[k][0]:recent[k]=(rank,Decimal(s))
    ids=sorted(k for k,(rank,v) in recent.items() if v>=50)
    return {'qualified_accounts':ids,'qualified_count':len(ids),'missing_rows':n}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
