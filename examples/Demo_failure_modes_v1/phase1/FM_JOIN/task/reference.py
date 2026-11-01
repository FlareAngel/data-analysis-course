import csv,json
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime
from zoneinfo import ZoneInfo

def solve(path=None):
    path=Path(path) if path else Path(__file__).resolve().parent/'data.csv'
    with path.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    return sum(float(r['amount']) for r in rows if r['record_type']=='order' and r['order_id'] in {p['order_id'] for p in rows if p['record_type']=='payment' and p['payment_status']=='success'})

if __name__=='__main__':
    print(json.dumps({'answer':solve()},ensure_ascii=False))
