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
    eligible=[r for r in rows if r['observed_at'][:4]=='2023' and r['region']=='NE' and r['source']=='AUTO']
    missing=0; latest={}
    for r in eligible:
        val=r['score_text'].strip()
        if val.upper() in ('','NULL','N/A'):missing+=1;continue
        key=(r['observed_at'],r['record_id'])
        if r['account_id'] not in latest or key>latest[r['account_id']][0]:latest[r['account_id']]=(key,Decimal(val))
    ids=sorted(acc for acc,(_,score) in latest.items() if score>=50)
    return {'high_score_accounts':ids,'high_score_count':len(ids),'excluded_missing_rows':missing}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
