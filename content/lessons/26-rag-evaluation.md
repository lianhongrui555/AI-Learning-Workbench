# 自建评测：命中率、引用覆盖率、延迟与完整度

> 本节作品：`evaluate.py` 和一份 Markdown/CSV 评测报告。
> 预计时间：80～110 分钟。
> 完成标准：至少 10 个测试问题生成 4 项指标和失败案例。

## 1. 创建测试问题集

新建 `data/eval_questions.json`：

```json
[
  {
    "question": "项目使用了哪些本地 AI 技术？",
    "keywords": ["Ollama", "Dify", "YOLO"]
  },
  {
    "question": "项目中有哪些工程日志？",
    "keywords": ["日志", "文档", "复盘"]
  }
]
```

至少补充到 10 条。运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 -m json.tool data\eval_questions.json
```

## 2. 创建 metrics.py

```python
def safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def hit_rate(answer: str, keywords: list[str]) -> float:
    hits = sum(1 for word in keywords if word.lower() in answer.lower())
    return safe_ratio(hits, len(keywords))


def citation_coverage(answer: str, sources: list[str]) -> float:
    cited = sum(1 for source in sources if source in answer)
    return safe_ratio(cited, len(sources))


def latency_score(latency_ms: int, max_ms: int = 10000) -> float:
    return max(0.0, 1.0 - safe_ratio(latency_ms, max_ms))


def completeness_score(answer: str, min_length: int = 30) -> float:
    return min(1.0, safe_ratio(len(answer), min_length))
```

## 3. 创建 evaluate.py

```python
import json
import csv
from pathlib import Path

import requests

from metrics import hit_rate, citation_coverage, latency_score, completeness_score

questions = json.loads(Path("data/eval_questions.json").read_text(encoding="utf-8"))
rows = []

for item in questions:
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": item["question"]},
        timeout=120,
    )
    data = response.json()
    row = {
        "question": item["question"],
        "hit_rate": hit_rate(data.get("answer", ""), item["keywords"]),
        "citation_coverage": citation_coverage(data.get("answer", ""), data.get("sources", [])),
        "latency_score": latency_score(data.get("latency_ms", 99999)),
        "completeness": completeness_score(data.get("answer", "")),
    }
    rows.append(row)
    print(row)

with Path("evaluation_report.csv").open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print("评测完成")
```

## 4. 运行评测

先确保 `/ask` 接口可用，再运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 evaluate.py
```

会生成：

```text
evaluation_report.csv
```

根据结果写一份 `evaluation_report.md`，至少包含：

- 平均命中率
- 平均引用覆盖率
- 平均延迟
- 失败问题列表
- 2 条优化建议

## 5. 代码填空

### 练习 1：补全安全除法

```python
def safe_ratio(numerator, denominator):
    # 补全安全除法
    pass
```

参考答案：

```python
def safe_ratio(numerator, denominator):
    return numerator / denominator if denominator else 0.0
```

### 练习 2：补全引用覆盖

```python
def citation_coverage(answer, sources):
    # 补全计算
    pass
```

参考答案：

```python
def citation_coverage(answer, sources):
    if not sources:
        return 0.0
    cited = sum(1 for source in sources if source in answer)
    return cited / len(sources)
```

## 6. 常见报错

- ZeroDivisionError：分母可能为 0。
- ConnectionError：接口未启动。
- 超时：调大 timeout 或减少问题数量。
- 文件找不到：检查 data 和输出目录。

## 7. 课后小测

1. 命中率衡量什么？
2. 引用覆盖率衡量什么？
3. 为什么质量和延迟要一起看？

## 8. 深度阅读

- [LlamaIndex Evaluation](https://developers.llamaindex.ai/python/framework/)
- [Microsoft Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners)