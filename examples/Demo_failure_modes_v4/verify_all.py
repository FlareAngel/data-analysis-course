from __future__ import annotations
import json,subprocess,sys,csv,importlib.util,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
allowed={"FM_REQUIREMENT","FM_SCHEMA","FM_DATA_TYPE","FM_FILTER_SORT","FM_JOIN","FM_AGGREGATION","FM_TIME_TIMEZONE","FM_MISSING_VALUE","FM_OUTLIER_BOUNDARY","FM_DUPLICATE_RECORD_HANDLING","FM_PLANNING_DECOMPOSITION","FM_VERIFICATION","FM_NUMERICAL_PRECISION_ROUNDING","FM_PROMPT_INJECTION"}
def strict_equal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(strict_equal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b
def run():
    outputs=[]
    for p in sorted((ROOT/'phase1').glob('*/task/task.json')):
        task=json.loads(p.read_text(encoding='utf-8'))
        assert task['hypothesized_failure_mode'] in allowed
        assert '东北' in task['description'] and '东北' in task['task_statement']
        assert set(task)=={'description','task_statement','hypothesized_failure_mode','answer'}
        assert isinstance(task['answer'],dict)
        assert '必须' in task['task_statement'] and 'JSON' in task['task_statement']
        with (p.parent/'data.csv').open(encoding='utf-8-sig',newline='') as f:
            records=list(csv.DictReader(f))
        assert records and 'region' in records[0]
        assert not any(r['region']=='东北' for r in records)
        proc=subprocess.run([sys.executable,str(p.parent/'reference.py')],capture_output=True,text=True,check=True)
        decoded=json.loads(proc.stdout)
        assert set(decoded)=={'answer'}
        assert strict_equal(decoded['answer'],task['answer'])
        # Reject plausible wrong JSON data types at nested value positions
        def wrong_type(v):
            if isinstance(v,bool):return str(v).lower()
            if isinstance(v,int):return str(v)
            if isinstance(v,float):return str(v)
            if isinstance(v,str):return 0
            if isinstance(v,list):return str(v)
            if isinstance(v,dict):return str(v)
            return 'null'
        for k,val in task['answer'].items():
            mutant=dict(task['answer']);mutant[k]=wrong_type(val)
            assert not strict_equal(mutant,task['answer'])
        spec=importlib.util.spec_from_file_location('test_reference',p.parent/'reference.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        assert strict_equal(module.reference()['answer'],task['answer'])
        outputs.append([p.parent.parent.name,task['hypothesized_failure_mode'],len(records),'PASS'])
    assert len(outputs)==14 and len({x[1] for x in outputs})==14
    for r in outputs:print(*r,sep=' | ')
    print(f'TOTAL: {len(outputs)}/14 PASS, no course runner claimed')
if __name__=='__main__':run()
