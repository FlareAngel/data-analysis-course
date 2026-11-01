import json,sys
from pathlib import Path

def check(expected, actual, path='$'):
    if type(expected) is not type(actual):return f'{path}: expected type {type(expected).__name__}, got {type(actual).__name__}'
    if isinstance(expected,dict):
        if set(expected)!=set(actual):return f'{path}: expected keys {sorted(expected)}, got {sorted(actual)}'
        for k in expected:
            result=check(expected[k],actual[k],path+'.'+k)
            if result:return result
    elif isinstance(expected,list):
        if len(expected)!=len(actual):return f'{path}: expected length {len(expected)}, got {len(actual)}'
        for i,(e,a) in enumerate(zip(expected,actual)):
            result=check(e,a,f'{path}[{i}]')
            if result:return result
    elif expected!=actual:return f'{path}: expected {expected!r}, got {actual!r}'
    return None

def main():
    if len(sys.argv)!=3:raise SystemExit('Usage: python validate_candidate.py TASK_ID candidate.json')
    task_id=sys.argv[1]
    src=Path(__file__).parent/'phase1'/task_id/'task'/'task.json'
    expected={'answer':json.loads(src.read_text(encoding='utf-8'))['answer']}
    try:actual=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    except (ValueError,OSError) as e:print('FAIL: invalid JSON',e);raise SystemExit(1)
    error=check(expected,actual)
    print('FAIL: '+error if error else 'PASS')
    raise SystemExit(1 if error else 0)
if __name__=='__main__':main()
