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
    tz=ZoneInfo('America/New_York')
    counts=[0,0]
    for r in rows:
        if not (r['region']=='NE' and r['event_type']=='PAYMENT_CAPTURED' and r['channel'] in ('WEB','APP')):continue
        local=datetime.fromisoformat(r['event_time'].replace('Z','+00:00')).astimezone(tz)
        if local.date().isoformat()=='2024-11-03' and local.hour==1: counts[local.fold]+=1
    return {'timezone':'America/New_York','local_date':'2024-11-03','hour':'01:00','first_occurrence':counts[0],'second_occurrence':counts[1],'total':sum(counts)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
