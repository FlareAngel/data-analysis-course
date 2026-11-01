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
    line_sum=defaultdict(lambda:Decimal(0));line_count=Counter()
    for r in rows:
        if r['row_type']=='LINE':line_sum[r['invoice_id']]+=Decimal(r['line_amount']);line_count[r['invoice_id']]+=1
    headers=[r for r in rows if r['row_type']=='HEADER' and r['invoice_date'][:4]=='2023' and r['region']=='NE' and r['state']=='POSTED']
    good=[];bad=[]
    for r in headers:
        ok=line_count[r['invoice_id']]>0 and line_sum[r['invoice_id']]==Decimal(r['declared_total'])
        (good if ok else bad).append(r['invoice_id'])
    good=sorted(set(good));bad=sorted(set(bad))
    return {'balanced_ids':good,'failed_ids':bad,'balanced_count':len(good),'failed_count':len(bad)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
