import csv,json
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime
from zoneinfo import ZoneInfo

def solve(path=None):
    path=Path(path) if path else Path(__file__).resolve().parent/'data.csv'
    with path.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    return sorted((r for r in rows if r['region']=='East' and r['status']=='active'),key=lambda r:(-float(r['score']),r['id']))[0]['id']

if __name__=='__main__':
    print(json.dumps({'answer':solve()},ensure_ascii=False))
