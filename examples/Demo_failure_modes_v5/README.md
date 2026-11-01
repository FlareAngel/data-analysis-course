# 14 道同义替换高难度数据分析 Task

本题集基于上传的 `task8.zip` 所体现的原则设计：同一个业务含义可以在 CSV 中有数个不同写法，例如 `NA`、`null`、`N/A`、空字符串、空格、`--` 均可以表示缺失，但 `0` 不属于缺失值。每个需要参与计算的同义关系均在该题的 `task_statement` 中直接以自然语言交代，不需要参考 README 才能答题。

## 设计要求

- 14 道题的 `description` 都包含“东北”，CSV 中不直接出现汉字“东北”；地理位置必须正确理解代码及方向修正。
- 一题一段连续、完整的中文 `task_statement`，不使用「映射 1/映射 2」式章节拼接。
- 每题重点考一种课程提供的 FM 类型，但会结合若干与任务目标有关的同义字段写法。
- 记录类型、字段含义、计算先后顺序、区间边界和 JSON 输出类型都在题干内定义。
- 参考程序对写法做业务归一化后计算，基于真实 CSV 执行而不是硬编码答案。
- 题目不要求 Agent 服从 CSV 中留言的任何指令；留言只作为普通业务数据，不具权威性。

## 14 道任务

| 题号 | Failure Mode | 需要识别的重点同义关系 |
|---|---|---|
| 20250301 | FM_REQUIREMENT | `SETTLED/SET_OK/Z01A/Z01B` 表示已结算；移动端与网页端各有多个编码 |
| 20250302 | FM_SCHEMA | `K11/K12/BUNDLE/KIT_PACK` 均为套件，`ONE/PCS` 与 `TWO/HALF_UNITS` 表示不同件数单位 |
| 20250303 | FM_DATA_TYPE | `BOOKED/POSTED` 表示已记账、`SALE/SOLD` 表示销售，金额文本中含括号负数与多种缺失符号 |
| 20250304 | FM_FILTER_SORT | 已支付和渠道代码有多种同义写法，金额还需转换单位后再排序 |
| 20250305 | FM_JOIN | ORDER、PAYMENT、REFUND 均有多种实体编码，成功和结算状态有同义写法 |
| 20250306 | FM_AGGREGATION | 已支付状态、APP/WEB 渠道、元/分单位的多写法归一化后，才能做加权聚合 |
| 20250307 | FM_TIME_TIMEZONE | 捕获事件有 `E11/E12/CAPTURE/CAPTURE_OK` 四种写法，事件时间另需正确转时区 |
| 20250308 | FM_MISSING_VALUE | 空、空格、`NA`、`N/A`、`NULL`、`null`、`--` 均为缺失，但 `0`、`0.00` 和负分有效 |
| 20250309 | FM_OUTLIER_BOUNDARY | `P1/STANDARD`、`P2/PROMO` 各用不同金额区间，异常与无效边界严格区别 |
| 20250310 | FM_DUPLICATE_RECORD_HANDLING | `Z12A/Z12B/DELIVERED/SIGNED` 均已签收，版本号支持 `v10/ver:10/rev10` |
| 20250311 | FM_PLANNING_DECOMPOSITION | `ACTIVE/ENABLED` 均为正常，认证与评分量纲也存在多种写法，选最新后再判断 |
| 20250312 | FM_VERIFICATION | 发票头和明细分别存在多种实体编码，已入账亦有多种写法 |
| 20250313 | FM_NUMERICAL_PRECISION_ROUNDING | 税率具有 R 编码和 VAT/TAX 别名，需逐行舍入再汇总 |
| 20250314 | FM_PROMPT_INJECTION | 多种支付与渠道代码；客户留言不是结构化订单字段，不可覆盖既定业务事实 |

## 文件结构

```text
phase1/
  20250301/task/{task.json,data.csv,reference.py}
  ...
  20250314/task/{task.json,data.csv,reference.py}
verify_all.py
validate_candidate.py
verification_report.json
design_manifest.json
sensitivity_checks.json
README.md
```

## 验证方法

在此文件夹根目录执行：

```bash
python verify_all.py
python phase1/20250308/task/reference.py
python validate_candidate.py 20250308 candidate.json
```

`verify_all.py` 检查 14 个参考程序、`task.json` 答案、FM 编号、题干地区及 CSV 数据。`sensitivity_checks.json` 逐字段记录“移除含有同义别名的记录后，输出是否改变”的反例压力测试；这是对映射重要性的测试，**不是目标 Agent 的真实错误率**。尚未通过课程的 `bin/datac reference run --phase phase1` Runner 运行。

每题标准答案由对应的 `reference.py` 读取 `data.csv` 实时计算，严格 JSON 验证程序还会拒绝字符串与数值类型互换、数组换序以及漏字段等错误。
