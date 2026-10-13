# RAG 查询引擎：检索、引用与 Prompt 组装

> 本节作品：带引用来源和耗时的 `/ask` FastAPI 接口。
> 预计时间：80～110 分钟。
> 完成标准：接口返回 answer、sources 和 latency_ms。

## 1. 在 rag.py 中封装查询

```python
import time
from llama_index.core import StorageContext, load_index_from_storage


def ask(question: str) -> dict:
    start = time.perf_counter()
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query(question)
    sources = []
    for node in response.source_nodes:
        sources.append(node.metadata.get("file_name", "unknown"))
    latency_ms = int((time.perf_counter() - start) * 1000)
    return {
        "answer": str(response),
        "sources": sorted(set(sources)),
        "latency_ms": latency_ms,
    }
```

先单独测试：

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "from rag import ask; print(ask('项目有哪些AI实践'))"
```

## 2. 设计回答 Prompt

在 `rag.py` 中给查询引擎加提示词约束：

```python
from llama_index.core import PromptTemplate

qa_prompt = PromptTemplate(
    "你只能根据下面的资料回答问题。\n"
    "如果资料中没有答案，请直接说不知道。\n"
    "回答后列出依据来源。\n"
    "资料：{context_str}\n"
    "问题：{query_str}\n"
)
```

实际使用时把它接到 query engine 的 text_qa_template。不同 LlamaIndex 版本的参数名可能不同，遇到报错时用 `/docs` 和官方文档核对。

## 3. 实现 /ask 接口

```python
from fastapi import FastAPI
from models import AskRequest, AskResponse
from rag import ask

app = FastAPI(title="AI Interview Assistant API")


@app.post("/ask", response_model=AskResponse)
def ask_api(request: AskRequest):
    result = ask(request.question)
    return AskResponse(**result)
```

运行：

```powershell
.\.venv\Scripts\uvicorn.exe app_fastapi:app --reload --port 8000
```

## 4. 测试接口

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType application/json -Body '{"question":"项目有哪些AI实践"}'
```

应返回结构：

```json
{
  "answer": "...",
  "sources": ["README.md"],
  "latency_ms": 1234
}
```

把一次结果写进笔记，记录回答、来源和耗时。

## 5. 调节 top_k

把 `similarity_top_k=3` 改成 1、5，分别观察：

- 回答内容变化。
- 引用数量变化。
- 耗时变化。

在笔记中写出结论。

## 6. 代码填空

### 练习 1：创建查询引擎

```python
query_engine = index.____()
```

参考答案：

```python
query_engine = index.as_query_engine(similarity_top_k=3)
```

### 练习 2：整理引用

```python
sources = []
for node in response.source_nodes:
    # 补全来源名称
    pass
```

参考答案：

```python
sources.append(node.metadata.get("file_name", "unknown"))
```

## 7. 常见报错

- `storage` 不存在：先完成第 21～22 节。
- 来源为空：检查 metadata 是否包含 file_name。
- 500：看终端堆栈，通常是 Prompt 模板参数名不匹配。
- 回答无关：检查切片大小和 top_k。

## 8. 课后小测

1. 索引和查询引擎分别负责什么？
2. 引用来源有什么价值？
3. top_k 调大有什么利弊？

## 9. 深度阅读

- [LlamaIndex Query Engine](https://developers.llamaindex.ai/python/framework/)
- [FastAPI 请求体](https://fastapi.tiangolo.com/tutorial/body/)