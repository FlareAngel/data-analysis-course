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
        key=(r['received_at'],int(r['version']),r['raw_id'])
        if r['event_id'] not in latest or key>latest[r['event_id']][0]:latest[r['event_id']]=(key,r)
    eligible=[r for _,r in latest.values() if r['event_date'][:4]=='2023' and r['region']=='NE' and r['state']=='DELIVERED']
    ids=sorted({r['order_id'] for r in eligible})
    return {'delivered_order_ids':ids,'distinct_order_count':len(ids),'retained_event_count':len(eligible)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
