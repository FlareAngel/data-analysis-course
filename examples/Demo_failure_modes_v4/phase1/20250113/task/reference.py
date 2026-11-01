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
    eligible=[r for r in rows if r['effective_date'][:4]=='2023' and r['region']=='NE' and r['state']=='POSTED']
    rounded=[(Decimal(r['taxable_amount'])*Decimal(r['tax_rate'])).quantize(TWO,rounding=ROUND_HALF_UP) for r in eligible]
    total=sum(rounded,Decimal(0));cents=total*100
    if cents!=cents.to_integral_value():raise ValueError('Cents not integer')
    return {'tax_yuan':money(total),'tax_cents':int(cents),'taxed_line_count':len(eligible)}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
