from __future__ import annotations
import csv
import json
from pathlib import Path
import re
from decimal import Decimal, ROUND_HALF_UP
from collections import Counter, defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

GEO_BASE = {'A1': 'NE', 'A2': 'NE', 'B1': 'NW', 'B2': 'NW', 'C1': 'SE', 'C2': 'SE', 'D1': 'SW', 'D2': 'SW', 'E1': 'CN', 'E2': 'CN'}
STATE_BASE = {'Z01A': 'SETTLED', 'Z01B': 'SETTLED', 'Z02A': 'PAID', 'Z02B': 'PAID', 'Z03A': 'PENDING', 'Z03B': 'PENDING', 'Z04A': 'REFUNDED', 'Z04B': 'REFUNDED', 'Z05A': 'VOID', 'Z05B': 'VOID', 'Z06A': 'UNPAID', 'Z06B': 'UNPAID', 'Z07A': 'CANCELLED', 'Z07B': 'CANCELLED', 'Z08A': 'SUCCESS', 'Z08B': 'SUCCESS', 'Z09A': 'FAILED', 'Z09B': 'FAILED', 'Z10A': 'REJECTED', 'Z10B': 'REJECTED', 'Z11A': 'DECLINED', 'Z11B': 'DECLINED', 'Z12A': 'DELIVERED', 'Z12B': 'DELIVERED', 'Z13A': 'IN_TRANSIT', 'Z13B': 'IN_TRANSIT', 'Z14A': 'RETURNED', 'Z14B': 'RETURNED', 'Z15A': 'ACTIVE', 'Z15B': 'ACTIVE', 'Z16A': 'SUSPENDED', 'Z16B': 'SUSPENDED', 'Z17A': 'POSTED', 'Z17B': 'POSTED', 'Z18A': 'DRAFT', 'Z18B': 'DRAFT'}
CHANNEL_BASE = {'M1': 'APP', 'M2': 'APP', 'W1': 'WEB', 'W2': 'WEB', 'S1': 'STORE', 'S2': 'STORE', 'P1': 'PARTNER', 'P2': 'PARTNER'}
SPECIAL_BASE = {'row_type': {'T11': 'ORDER', 'T12': 'ORDER', 'T21': 'PAYMENT', 'T22': 'PAYMENT', 'T31': 'REFUND', 'T32': 'REFUND', 'T41': 'HEADER', 'T42': 'HEADER', 'T51': 'LINE', 'T52': 'LINE'}, 'sku': {'K11': 'KIT', 'K12': 'KIT', 'K21': 'BOOK', 'K22': 'BOOK', 'K31': 'FEE', 'K32': 'FEE'}, 'is_posted': {'F11': '1', 'F12': '1', 'F21': '0', 'F22': '0'}, 'kind': {'B11': '销售', 'B12': '销售', 'B21': '调整', 'B22': '调整'}, 'event_type': {'E11': 'PAYMENT_CAPTURED', 'E12': 'PAYMENT_CAPTURED', 'E21': 'PAYMENT_CREATED', 'E22': 'PAYMENT_CREATED', 'E31': 'PAYMENT_FAILED', 'E32': 'PAYMENT_FAILED'}, 'source': {'U11': 'AUTO', 'U12': 'AUTO', 'U21': 'MANUAL', 'U22': 'MANUAL'}, 'kyc': {'V11': 'KYC_OK', 'V12': 'KYC_OK', 'V21': 'KYC_WAIT', 'V22': 'KYC_WAIT'}, 'tax_rate': {'R05A': '0.05', 'R05B': '0.05', 'R075A': '0.075', 'R075B': '0.075', 'R10A': '0.10', 'R10B': '0.10', 'R125A': '0.125', 'R125B': '0.125'}}
RAW_SPECIAL = {'row_type': 'entity_code', 'sku': 'item_code', 'is_posted': 'ledger_code', 'kind': 'business_code', 'event_type': 'action_code', 'source': 'source_code', 'kyc': 'kyc_code', 'tax_rate': 'rate_code'}
MONETARY = []
TWO=Decimal('0.01')

def money(val):
    return format(Decimal(val).quantize(TWO,rounding=ROUND_HALF_UP), '.2f')

def swap_direction(region, direction):
    if region=='CN':
        if direction!='NONE': raise ValueError('CN direction must be NONE')
        return region
    if direction=='NONE': return region
    if direction=='FLIP_EW': return region[0]+('W' if region[1]=='E' else 'E')
    if direction=='FLIP_NS': return ('S' if region[0]=='N' else 'N')+region[1]
    raise ValueError('unknown geographic adjustment: '+direction)

def decode_amount(raw, unit):
    if raw=='': return ''
    val=Decimal(raw)
    if unit=='CENT': val=val/100
    elif unit!='YUAN':raise ValueError('invalid money_unit '+unit)
    return str(val)

def decode_special_amount(raw, unit):
    s=raw.strip()
    if s in ('—',''): return s
    is_negative=s.startswith('(') and s.endswith(')')
    if is_negative:s=s[1:-1]
    val=Decimal(s.replace(',','').removeprefix('+'))
    if is_negative:val=-val
    if unit=='CENT': val=val/100
    elif unit!='YUAN': raise ValueError('money unit')
    return str(val)

def is_kept(r):
    main = r['record_class'] in ('L1','L2')
    flag=r['override_code']
    if flag=='FORCE_KEEP': return True
    if flag=='FORCE_DROP': return False
    if flag!='NONE': raise ValueError('unknown override')
    return main

def normalize(rows):
    out=[]
    for r in rows:
        if not is_kept(r): continue
        x={k:v for k,v in r.items() if k not in ('geo_ref','geo_adjust','record_class','override_code','money_unit')}
        geo=GEO_BASE[r['geo_ref']]
        x['region']=swap_direction(geo,r['geo_adjust'])
        if 'status_code' in x:
            x['status']=STATE_BASE[x.pop('status_code')]
        if 'state_code' in x:
            x['state']=STATE_BASE[x.pop('state_code')]
        if 'touch_code' in x:
            x['channel']=CHANNEL_BASE[x.pop('touch_code')]
        for src,target in RAW_SPECIAL.items():
            if target in x:
                value=x.pop(target)
                x[src]=SPECIAL_BASE[src][value] if value else ''
        for col in MONETARY:
            if col in x:
                if col=='amount_text': x[col]=decode_special_amount(x[col], r['money_unit'])
                else: x[col]=decode_amount(x[col],r['money_unit'])
        if 'qty_encoded' in x:
            q=Decimal(x.pop('qty_encoded'))
            u=x.pop('qty_unit')
            if u=='TWO':q=q/2
            elif u!='ONE':raise ValueError('invalid quantity unit')
            if q!=int(q):raise ValueError('nonintegral qty')
            x['qty']=str(int(q))
        if 'score_unit' in x:
            unit=x.pop('score_unit')
            if 'score_text' in x:
                s=x['score_text'].strip()
                if s and s.upper() not in ('NULL','N/A') and unit=='CENTIPOINT':x['score_text']=str(Decimal(s)/100)
            if 'score' in x:
                if unit=='CENTIPOINT':x['score']=str(int(x['score'])//100)
            if unit not in ('POINT','CENTIPOINT'):raise ValueError('score unit')
        if 'version_encoded' in x:x['version']=str(int(x.pop('version_encoded')[1:]))
        if 'seq_encoded' in x:x['seq']=str(int(x.pop('seq_encoded')[1:]))
        out.append(x)
    return out


# 原始 CSV 允许一个业务值使用多种写法，先统一为标准编码，再执行统计。
ALIASES = {'geo_ref': {'NE-A': 'A1', 'NE-B': 'A2'}, 'geo_adjust': {'STAY': 'NONE', 'SWAP_EW': 'FLIP_EW', 'SWAP_NS': 'FLIP_NS'}, 'override_code': {'AUTO': 'NONE', 'KEEP': 'FORCE_KEEP', 'DROP': 'FORCE_DROP'}, 'state_code': {'DELIVERED': 'Z12A', 'SIGNED': 'Z12B'}}

def canonicalize_raw(row):
    row = dict(row)
    for field, aliases in ALIASES.items():
        if field not in row:
            continue
        val = row[field]
        row[field] = aliases.get(val, val)
    if 'score_text' in row and row['score_text'].strip().lower() in ('na','n/a','null','--'):
        row['score_text'] = 'NULL'
    if 'amount_text' in row and row['amount_text'].strip().lower() in ('na','n/a','null',''):
        row['amount_text'] = '—'
    if 'version_encoded' in row:
        row['version_encoded'] = re.sub(r'^(?:ver:|rev)', 'v', row['version_encoded'])
    if 'seq_encoded' in row:
        row['seq_encoded'] = re.sub(r'^(?:seq:|rev)', 's', row['seq_encoded'])
    return row

def reference(df=None):
    if df is None:
        with open(Path(__file__).with_name('data.csv'),encoding='utf-8-sig',newline='') as f:
            raw=list(csv.DictReader(f))
    else:
        raw=df.fillna('').astype(str).to_dict(orient='records')
    raw = [canonicalize_raw(r) for r in raw]
    return {'answer':solve(normalize(raw))}


def solve(rows):
    latest={}
    for r in rows:
        key=(r['received_at'],int(r['version']),r['raw_id'])
        if r['event_id'] not in latest or key>latest[r['event_id']][0]:latest[r['event_id']]=(key,r)
    eligible=[r for _,r in latest.values() if r['event_date'][:4]=='2023' and r['region']=='NE' and r['state']=='DELIVERED']
    ids=sorted({r['order_id'] for r in eligible})
    return {'delivered_order_ids':ids,'distinct_order_count':len(ids),'retained_event_count':len(eligible)}

if __name__ == '__main__':
    print(json.dumps(reference(),ensure_ascii=False,allow_nan=False,separators=(',',':')))
