import csv,json
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime
from zoneinfo import ZoneInfo

def solve(path=None):
    path=Path(path) if path else Path(__file__).resolve().parent/'data.csv'
    with path.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    return sum(datetime.fromisoformat(r['timestamp_utc'].replace('Z','+00:00')).astimezone(ZoneInfo('America/Los_Angeles')).date().isoformat()=='2025-03-09' for r in rows)

if __name__=='__main__':
    print(json.dumps({'answer':solve()},ensure_ascii=False))
