from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def _strict_json(raw):
    def no_constants(v):raise ValueError('Non-finite JSON value: '+v)
    def no_dups(pairs):
        out={}
        for k,v in pairs:
            if k in out:raise ValueError('Repeated JSON object key: '+k)
            out[k]=v
        return out
    return json.loads(raw,parse_constant=no_constants,object_pairs_hook=no_dups)

def strict_equal(a,b,path='$'):
    if type(a) is not type(b):
        return False,f'{path}: expected {type(b).__name__}, got {type(a).__name__}'
    if isinstance(a,dict):
        if set(a)!=set(b):return False,f'{path}: expected keys {sorted(b)}, got {sorted(a)}'
        for key in b:
            valid,reason=strict_equal(a[key],b[key],f'{path}.{key}')
            if not valid:return valid,reason
    elif isinstance(a,list):
        if len(a)!=len(b):return False,f'{path}: expected array length {len(b)}, got {len(a)}'
        for i,(value,expected) in enumerate(zip(a,b)):
            valid,reason=strict_equal(value,expected,f'{path}[{i}]')
            if not valid:return valid,reason
    elif a!=b:return False,f'{path}: value differs'
    return True,'matched'

def validate(task_id, candidate_path):
    if not(task_id.isdigit() and len(task_id)==8):return False,'task_id must be 8 digits'
    source=ROOT/'phase1'/task_id/'task'/'task.json'
    if not source.exists():return False,'unknown task id'
    task=_strict_json(source.read_text(encoding='utf-8'))
    candidate=_strict_json(Path(candidate_path).read_text(encoding='utf-8-sig'))
    return strict_equal(candidate,{'answer':task['answer']})

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python validate_candidate.py TASK_ID candidate.json')
    try:good,reason=validate(sys.argv[1],sys.argv[2])
    except (ValueError,OSError,json.JSONDecodeError) as error:good,reason=False,str(error)
    print(('PASS' if good else 'FAIL')+': '+reason)
    raise SystemExit(0 if good else 1)
