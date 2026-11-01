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
    eligible=[r for r in rows if r['created_at'][:4]=='2023' and r['region']=='NE' and r['status']=='PAID' and r['channel'] in ('WEB','APP')]
    eligible.sort(key=lambda r:(-Decimal(r['amount']),r['created_at'],r['invoice_id']))
    seven=eligible[:7]
    if len(seven)!=7: raise ValueError('Insufficient eligible invoices')
    return {'top7_invoice_ids':[r['invoice_id'] for r in seven],'rank7':{'invoice_id':seven[6]['invoice_id'],'amount':money(seven[6]['amount'])}}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
