import csv, json
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
from zoneinfo import ZoneInfo

def records():
    with (Path(__file__).parent/'data.csv').open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def dt(x):
    return datetime.fromisoformat(x.replace('Z','+00:00'))

def money(x):
    return Decimal(x or '0')

def cents(x):
    return str(Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

def solve(data,variant=False):
    rates=defaultdict(list)
    alias={'USD':'USD','US$':'USD','EUR':'EUR','EURO':'EUR'}
    for r in data:
        if r['entity']=='RATE':rates[alias[r['currency']]].append((date.fromisoformat(r['effective_date']),money(r['rate_to_usd'])))
    for vals in rates.values():vals.sort()
    tz=ZoneInfo('America/Los_Angeles');amount=Decimal(0);n=0
    for r in data:
        if r['entity']!='TXN' or r['region'] not in ('NE','N-E') or r['status'] not in ('PAID','OK'):continue
        day=dt(r['occurred_at']).date() if variant else dt(r['occurred_at']).astimezone(tz).date()
        if day!=date(2024,3,10):continue
        valid=[rate for d,rate in rates[alias[r['currency']]] if d<=day]
        if not valid:continue
        n+=1;amount+=money(r['amount'])*valid[-1]
    return {'txn_count':n,'total_usd':cents(amount)}

if __name__=="__main__":
    print(json.dumps({"answer":solve(records())},ensure_ascii=False))
