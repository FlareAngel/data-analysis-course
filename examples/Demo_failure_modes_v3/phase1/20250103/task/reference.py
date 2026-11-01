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
    group=[r for r in rows if r['txn_date'][:4]=='2023' and r['region']=='NE' and r['is_posted']=='1' and r['kind']=='销售']
    net=Decimal(0); neg=missing=0
    for r in group:
        raw=r['amount_text'].strip()
        if raw=='—':
            missing+=1; continue
        isneg=raw.startswith('(') and raw.endswith(')')
        if isneg: raw=raw[1:-1]
        val=Decimal(raw.replace(',','').removeprefix('+'))
        if isneg: val=-val
        neg+=val<0
        net+=val
    cents=net*100
    if cents!=cents.to_integral_value(): raise ValueError('Expected exact cents')
    return {'net_cents':int(cents),'negative_row_count':neg,'missing_row_count':missing}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
