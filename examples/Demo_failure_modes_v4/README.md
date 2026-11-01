# 高难度 JSON 严格输出 Task：14 种标准 Failure Mode

这是一套**新任务**（`20250101`–`20250114`），沿用上一批已验证的合成 CSV 作为难度基线，并改写计算输出要求，测试 Agent 的语义映射、计算口径、输出 JSON 类型与精确结构一致性。

- 每题包含 `task.json`、`data.csv`、独立可执行的 `reference.py`。所有 description 都包括“东北”，CSV `region` 字段仍使用 `NE` 等编码。
- 格式约束是**显式可判定的业务接口契约**，不检查 JSON 对象键的排列顺序、无意义的空格或换行；只检查 JSON 语义值和类型、数组顺序以及结构。
- 顶层输出永远是 `{"answer": ...}`，**`answer` 内部严格遵循每题指定的数据类型**。`task.json` 内的 answer 为该内部值，参考程序打印整个顶层 JSON。
- 不添加恶意指令或故意含糊的隐藏约定。`FM_PROMPT_INJECTION` 使用普通客户意见文本作为非权威数据字段，而非攻击 Agent 的指令。
- 这套数据为合成数据，不暗示真实企业结果。并没有模拟真实 Agent 运行结果或谎称 Agent 必然失败。

## 运行与核对

```bash
python phase1/20250101/task/reference.py
python verify_all.py
```

`verify_all.py` 对14题进行全量验证：程序可运行、task.json 有效、实际输出与 `answer` 严格类型相等、schema 基本不变量、地区文字要求、以及反例格式是否能被严格类型验证拒绝。

**课程兼容性提示**：课程专用 `bin/datac reference run --phase phase1` 未在此环境验证。课程 Runner 如限定 `answer` 必须为数字而不支持对象，则复杂 JSON 输出契约需要配套评测器支持，不能仅凭参考程序成功宣称课程 PASS。

## 针对上传的旧 Task

上传的 `task11.zip` 的题意为先按用户最大订单额聚合、再求均值并输出 JSON；其 `task.json` 存在无效 JSON 拼接/逗号问题，且未含 `answer`。本套任务以**合法、可运行、数据类型明确且可自动检查**为前提修订。

## 主要输出陷阱

| Task | Failure Mode | 输出结构重点 |
|---|---|---|
| 20250101 | `FM_REQUIREMENT` | answer 必须是对象，恰有 {"region":"东北","channels":["APP","WEB"],"order_count":整数,"net_amount":"带两位小数的十进制字符 |
| 20250102 | `FM_SCHEMA` | answer 必须是对象，恰有 {"qualified_customer_count":整数,"customers":[{"customer_id":字符串,"distinct_orders":整 |
| 20250103 | `FM_DATA_TYPE` | answer 必须是对象，恰有 {"net_cents":整数,"negative_row_count":整数,"missing_row_count":整数}，所有值都是 JSON 整数（包括负整 |
| 20250104 | `FM_FILTER_SORT` | answer 必须是对象，恰有 {"top7_invoice_ids":[7个字符串],"rank7":{"invoice_id":字符串,"amount":"恰好两位小数的金额字符串"}} |
| 20250105 | `FM_JOIN` | answer 必须是对象，恰有 {"settled_order_count":整数,"successful_payment_count":整数,"successful_refund_count": |
| 20250106 | `FM_AGGREGATION` | answer 必须是对象，恰有 {"basis_amount":"两位小数的字符串","discount_amount":"两位小数的字符串","discount_rate_pct":数字} |
| 20250107 | `FM_TIME_TIMEZONE` | answer 必须是对象，恰有 {"timezone":"America/New_York","local_date":"2024-11-03","hour":"01:00","first_occ |
| 20250108 | `FM_MISSING_VALUE` | answer 必须是对象，恰有 {"high_score_accounts":[字符串,...],"high_score_count":整数,"excluded_missing_rows":整数} |
| 20250109 | `FM_OUTLIER_BOUNDARY` | answer 必须是对象，恰有 {"below":整数,"within":整数,"above":整数,"has_lower_boundary":布尔值,"has_upper_boundary":布 |
| 20250110 | `FM_DUPLICATE_RECORD_HANDLING` | answer 必须是对象，恰有 {"delivered_order_ids":[字符串,...],"distinct_order_count":整数,"retained_event_count": |
| 20250111 | `FM_PLANNING_DECOMPOSITION` | answer 必须是对象，恰有 {"latest_account_count":整数,"qualified_count":整数,"qualified_ids":[字符串,...]} |
| 20250112 | `FM_VERIFICATION` | answer 必须是对象，恰有 {"balanced_ids":[字符串,...],"failed_ids":[字符串,...],"balanced_count":整数,"failed_count |
| 20250113 | `FM_NUMERICAL_PRECISION_ROUNDING` | answer 必须是对象，恰有 {"tax_yuan":"恰好两位小数的数字字符串","tax_cents":整数,"taxed_line_count":整数} |
| 20250114 | `FM_PROMPT_INJECTION` | answer 必须是对象，恰有 {"APP":{"orders":整数,"amount":"两位小数字符串"},"WEB":{"orders":整数,"amount":"两位小数字符串"},"to |

## 单个 Agent 答案的严格校验

将 Agent 原始回复保存为 `candidate.json`，然后执行：

```bash
python validate_candidate.py 20250101 candidate.json
```

校验器解析**整个响应**为 JSON 并拒绝重复键、NaN/Infinity、额外键、漏键、错误的数据类型、数组次序、数值不一致。与任意有效 JSON 一样，空格、缩进和对象键次序不影响判定。注意候选文件不得包含 Markdown 代码围栏或者解释文字。

本题组中 `NE` **不是直接写在题干的筛选值**；题目只提供方向字母规则，由解题者组合推导。14 份 CSV 文件均不包含“东北”这个中文词；`region` 列全部为字母缩写。
