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
    vals=[Decimal(r['amount']) for r in rows if r['txn_date'][:4]=='2023' and r['region']=='NE' and r['channel'] in ('WEB','APP') and r['state']=='SUCCESS']
    lo,hi=Decimal('20'),Decimal('200')
    return {'below':sum(v<lo for v in vals),'within':sum(lo<=v<=hi for v in vals),'above':sum(v>hi for v in vals),'has_lower_boundary':lo in vals,'has_upper_boundary':hi in vals}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
