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
    qualified={(r['customer_id'],r['order_id']) for r in rows if r['order_date'][:4]=='2023' and r['region']=='NE' and r['status']=='PAID' and r['sku']=='KIT' and int(r['qty'])>=2}
    freq=Counter(customer for customer,order in qualified)
    customers=[{'customer_id':c,'distinct_orders':freq[c]} for c in sorted(freq) if freq[c]>=2]
    return {'qualified_customer_count':len(customers),'customers':customers}

if __name__ == '__main__':
    print(json.dumps(reference(), ensure_ascii=False, allow_nan=False, separators=(',',':')))
