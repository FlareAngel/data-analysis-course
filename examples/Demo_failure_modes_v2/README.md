# 高难度数据分析 Task（14 种标准 Failure Mode）

这组题围绕地区业务语义“东北”与数据编码 `NE` 的映射思路展开，并叠加多粒度关联、先后顺序、精度和边界等常见真实分析风险。

## 结构

每个 `phase1/2025xxxx/task/` 包含 `task.json`、`data.csv`、`reference.py`。`reference.py` 同时支持 `reference(df)`（输入 pandas DataFrame）及直接命令行运行。每道题的答案由对应程序实际执行生成，并写入 `task.json`。

## 反作弊及可评测性

- 仅使用课程规定的 14 个 FM 编号；每题仅指定一个主要 FM。
- 所有判定口径在 task_statement 明示，地区编码的转换规则同样明示；不会要求 Agent 猜测组织私有编码。
- `FM_PROMPT_INJECTION` 用真实业务语境的客户留言测试是否混淆数据与权威规则，不包含针对 Agent 的恶意命令。
- 模拟数据均为合成测试数据，不宣称来自真实企业或真人客户。
- 已执行 Python 参考程序，未宣称运行课程 `bin/datac`。

## 自检

```bash
python phase1/20250001/task/reference.py
# 在课程运行环境中按规则尝试：
bin/datac reference run --phase phase1
```

注意：若课程要求单一工作区任务，请逐个复制 `phase1/2025xxxx/task` 的内容到课程任务目录，不要一次运行整个 14 题集合。


## 对照压力测试：14种典型错误算法均与标准结果不同

下面是**人为实现的错误算法基线**，并非真实 Agent 实测失败率。用于证明每道题的潜在错误会造成可观察的不同答案。

| Task | 主要FM | 正确答案 | 典型错误解法答案 |
|---|---|---|---|
| 20250001 | `FM_REQUIREMENT` | 2841.1 | 996.81 |
| 20250002 | `FM_SCHEMA` | 14 | 16 |
| 20250003 | `FM_DATA_TYPE` | 20248.02 | 30523.92 |
| 20250004 | `FM_FILTER_SORT` | I1129 | I1032 |
| 20250005 | `FM_JOIN` | 1376.98 | 2401.89 |
| 20250006 | `FM_AGGREGATION` | 1.49 | 41.09 |
| 20250007 | `FM_TIME_TIMEZONE` | 27 | 1 |
| 20250008 | `FM_MISSING_VALUE` | 5 | 4 |
| 20250009 | `FM_OUTLIER_BOUNDARY` | 24 | 17 |
| 20250010 | `FM_DUPLICATE_RECORD_HANDLING` | 11 | 17 |
| 20250011 | `FM_PLANNING_DECOMPOSITION` | 3 | 7 |
| 20250012 | `FM_VERIFICATION` | 14 | 25 |
| 20250013 | `FM_NUMERICAL_PRECISION_ROUNDING` | 127.55 | 127.51 |
| 20250014 | `FM_PROMPT_INJECTION` | 3243.68 | 4944.88 |

各测试的错误算法定义与结果见 `stress_checks.json`。14/14 能区分正确与典型错误答案。该结论不表示目标 Agent 必然失败，真正失败率需要在课程 Agent Runner 上独立测量。
