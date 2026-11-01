"""运行所有参考程序，并检查标准答案、题目结构与地区语义。无第三方依赖。"""
import csv,json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
VALID_FM = ['FM_REQUIREMENT','FM_SCHEMA','FM_DATA_TYPE','FM_FILTER_SORT',
            'FM_JOIN','FM_AGGREGATION','FM_TIME_TIMEZONE','FM_MISSING_VALUE',
            'FM_OUTLIER_BOUNDARY','FM_DUPLICATE_RECORD_HANDLING',
            'FM_PLANNING_DECOMPOSITION','FM_VERIFICATION',
            'FM_NUMERICAL_PRECISION_ROUNDING','FM_PROMPT_INJECTION']

def main():
    records=[]
    tasks=sorted((ROOT/'phase1').glob('*/task'))
    assert len(tasks)==14, f'预期14题，发现{len(tasks)}题'
    for taskdir in tasks:
        meta=json.loads((taskdir/'task.json').read_text(encoding='utf-8'))
        assert set(('description','task_statement','hypothesized_failure_mode','answer')) <= meta.keys()
        fm=meta['hypothesized_failure_mode']
        assert fm in VALID_FM
        assert '东北' in meta['description']
        assert '\n' not in meta['task_statement']
        assert '映射 1' not in meta['task_statement']
        assert '仅输出合法JSON' in meta['task_statement']
        data=(taskdir/'data.csv').read_text(encoding='utf-8')
        assert '东北' not in data
        with (taskdir/'data.csv').open(encoding='utf-8',newline='') as f:
            rows=list(csv.DictReader(f))
        assert len(rows)>=200
        run=subprocess.run([sys.executable,str(taskdir/'reference.py')],capture_output=True,text=True,check=True)
        result=json.loads(run.stdout)
        assert result=={'answer':meta['answer']},f'{taskdir.parent.name} 答案不一致'
        records.append({'task':taskdir.parent.name,'fm':fm,'rows':len(rows),'status':'PASS'})
        print(taskdir.parent.name,fm,len(rows),'PASS')
    assert sorted(x['fm'] for x in records)==sorted(VALID_FM)
    report={'status':'PASS','task_count':len(tasks),'total_rows':sum(x['rows'] for x in records),'records':records,
            'runner_scope':'独立执行reference.py；未运行课程bin/datac'}
    (ROOT/'verification_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('ALL PASS',len(records),report['total_rows'])

if __name__=='__main__':main()
