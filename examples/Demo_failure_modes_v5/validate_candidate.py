from __future__ import annotations
import json,sys
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parent

def reject_duplicates(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate key: '+k)
        d[k]=v
    return d

def strict_equal(a,b,path='$'):
    if type(a) is not type(b):return (False,f'{path}: type {type(a).__name__} != {type(b).__name__}')
    if isinstance(a,dict):
        if set(a)!=set(b):return (False,f'{path}: keys differ; missing={set(b)-set(a)}, extra={set(a)-set(b)}')
        for k in b:
            ok,msg=strict_equal(a[k],b[k],path+'.'+k)
            if not ok:return ok,msg
    elif isinstance(a,list):
        if len(a)!=len(b):return False,f'{path}: list length {len(a)} != {len(b)}'
        for i,(x,y) in enumerate(zip(a,b)):
            ok,msg=strict_equal(x,y,f'{path}[{i}]')
            if not ok:return ok,msg
    elif a!=b:return False,f'{path}: value {a!r} != {b!r}'
    return True,'PASS'

def load_json(text):
    def forbid(s):raise ValueError('nonstandard JSON number '+s)
    return json.loads(text,object_pairs_hook=reject_duplicates,parse_constant=forbid)

def check(task_id,raw):
    p=ROOT/'phase1'/task_id/'task'/'task.json'
    gold=json.loads(p.read_text(encoding='utf-8'))['answer']
    incoming=load_json(raw)
    return strict_equal(incoming,{'answer':gold})

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python validate_candidate.py <task_id> <candidate.json>')
    try:
        ok,msg=check(sys.argv[1],Path(sys.argv[2]).read_text(encoding='utf-8'))
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        ok,msg=False,str(exc)
    print('PASS' if ok else 'FAIL',msg)
    sys.exit(0 if ok else 1)
