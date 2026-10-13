# 工具调用与面试题 Agent

> 本节作品：能随机抽题、分类和结构化返回面试题的 Agent 接口。
> 预计时间：90～120 分钟。
> 完成标准：`/agent` 能调用工具并返回题目、分类和工具调用记录。

## 1. 创建 tools.py

```python
import random


QUESTIONS = [
    {"id": 1, "category": "RAG", "difficulty": "基础", "question": "RAG 的完整流程是什么？"},
    {"id": 2, "category": "Agent", "difficulty": "基础", "question": "Agent 为什么需要工具 Schema？"},
    {"id": 3, "category": "Ollama", "difficulty": "基础", "question": "Ollama 默认端口是多少？"},
]


def list_categories():
    return sorted({item["category"] for item in QUESTIONS})


def pick_question(category: str | None = None):
    pool = QUESTIONS if not category else [item for item in QUESTIONS if item["category"] == category]
    return random.choice(pool)


def classify_question(text: str):
    categories = list_categories()
    return next((item for item in categories if item.lower() in text.lower()), "未分类")
```

测试：

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "from tools import pick_question; print(pick_question())"
```

## 2. 工具输入输出规则

每个工具都应该写清楚：

- 名称：例如 `pick_question`
- 作用：随机抽取面试题
- 参数：`category`，可选
- 返回：题目、分类、难度

结构化返回比只返回一段文字更适合 Agent，因为后续可以继续分类、评分和记录。

## 3. 创建最小 Agent 逻辑

先用纯 Python 跑通一个“伪 Agent 循环”：

```python
def run_task(task: str):
    if "随机" in task and "题" in task:
        tool = "pick_question"
        result = pick_question()
    else:
        tool = "none"
        result = {"message": "暂时只支持随机抽题"}
    return {"task": task, "tool": tool, "result": result, "max_iterations": 3}
```

测试：

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "from tools import run_task; print(run_task('随机抽一道RAG题'))"
```

## 4. 接入 LlamaIndex Agent

不同 LlamaIndex 版本的 Agent API 名称可能不同。先阅读当前安装版本的示例，再按下面思路接入：

1. 从 LlamaIndex 导入 FunctionAgent 或 ReActAgent。
2. 把 `pick_question`、`list_categories` 注册为工具。
3. 设置 `max_iterations=3`。
4. 使用本地 Ollama 模型。
5. 在 `/agent` 接口中调用 Agent。

如果本地模型不稳定，可以先保留第 3 步的纯 Python 逻辑，等模型工具调用能力确认后再替换。

## 5. 增加 /agent 接口

```python
from fastapi import FastAPI
from pydantic import BaseModel
from tools import run_task

app = FastAPI(title="AI Interview Agent")

class AgentRequest(BaseModel):
    task: str

@app.post("/agent")
def agent_api(request: AgentRequest):
    return run_task(request.task)
```

测试：

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/agent -Method Post -ContentType application/json -Body '{"task":"随机抽一道RAG题"}'
```

## 6. 代码填空

### 练习 1：补全随机抽题

```python
import random

def pick_question(items):
    # 返回随机题目
    pass
```

参考答案：

```python
import random

def pick_question(items):
    return random.choice(items)
```

### 练习 2：补全工具参数

```python
def classify_question(question):
    return {"question": question, "category": "RAG"}
```

参考答案：

```python
def classify_question(question: str):
    return {"question": question, "category": "RAG"}
```

## 7. 常见报错

- 工具没有注册：检查工具列表和名称。
- 模型不调用工具：简化任务，先做规则版。
- 无限循环：设置 `max_iterations`。
- 参数类型错误：工具 Schema 和函数签名要一致。

## 8. 课后小测

1. 工具 Schema 对 Agent 有什么用？
2. 为什么需要最大步数？
3. 工具返回结构化数据有什么好处？

## 9. 深度阅读

- [LlamaIndex Agents](https://developers.llamaindex.ai/python/framework/)
- [Microsoft Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners)