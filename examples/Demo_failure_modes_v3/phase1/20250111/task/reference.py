from __future__ import annotations
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter, defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

TWO = Decimal('0.01')
def money(value):
    return format(Decimal(value).quantize(TWO, rounding=ROUND_HALF_UP), '.2f')

def reference(df=None):
    """Returns {'answer': JSON value}. Optional pandas DataFrame accepted."""
    if df is None:
        with open(Path(__file__).with_name('data.csv'), encoding='utf-8-sig', newline='') as handle:
            rows=list(csv.DictReader(handle))
    else:
        rows=df.fillna('').astype(str).to_dict(orient='records')
    return {'answer': solve(rows)}



def solve(rows):
    latest={}
    for r in rows:
        if not(r['event_time'][:4]=='2023' and r['region']=='NE'):continue
        key=(r['event_time'],int(r['seq']),r['event_id'])
        if r['account_id'] not in latest or key>latest[r['account_id']][0]:latest[r['account_id']]=(key,r)
    ids=sorted(r['account_id'] for _,r in latest.values() if r['state']=='ACTIVE' and r['kyc']=='KYC_OK' and int(r['score'])>=80)
    return {'latest_account_count':len(latest),'qualified_count':len(ids),'qualified_ids':ids}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
