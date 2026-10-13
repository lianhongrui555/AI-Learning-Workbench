# 会话记忆与流式输出

> 本节作品：支持 `conversation_id` 和流式返回的 `/ask/stream`。
> 预计时间：80～110 分钟。
> 完成标准：同一会话第二问能引用第一问，流式接口能逐步返回内容。

## 1. 创建 memory.py

```python
from collections import defaultdict

history_store = defaultdict(list)


def add_message(conversation_id: str, role: str, content: str):
    history_store[conversation_id].append({"role": role, "content": content})
    history_store[conversation_id] = history_store[conversation_id][-10:]


def get_history(conversation_id: str) -> list[dict]:
    return history_store.get(conversation_id, [])
```

测试：

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "from memory import add_message,get_history; add_message('c1','user','你好'); print(get_history('c1'))"
```

## 2. 把历史接入查询

在 `/ask` 中：

```python
from memory import add_message, get_history

history = get_history(request.conversation_id or "default")
history_text = "\n".join(f"{item['role']}: {item['content']}" for item in history)
question = f"历史对话：\n{history_text}\n\n当前问题：{request.question}"
result = ask(question)
add_message(request.conversation_id or "default", "user", request.question)
add_message(request.conversation_id or "default", "assistant", result["answer"])
```

测试：同一个 `conversation_id` 连续问两次，第二问应能引用第一问。

## 3. 普通 JSON 与流式返回的差异

普通 `/ask`：

```text
等模型全部生成完 → 一次性返回 JSON
```

流式 `/ask/stream`：

```text
模型生成一点 → 浏览器显示一点 → 直到结束
```

流式不能直接 `return {"answer": ...}`，需要使用 `StreamingResponse`。

## 4. 写流式接口

```python
import time
from fastapi.responses import StreamingResponse
from models import AskRequest


async def generate_text(question: str):
    # 这里用逐字模拟。接入 LlamaIndex streaming 后换成真实模型事件。
    text = f"你问的是：{question}"
    for char in text:
        yield char
        time.sleep(0.02)


@app.post("/ask/stream")
async def ask_stream(request: AskRequest):
    return StreamingResponse(
        generate_text(request.question),
        media_type="text/plain; charset=utf-8",
    )
```

## 5. 测试流式

```powershell
curl.exe -N -X POST http://127.0.0.1:8000/ask/stream -H "Content-Type: application/json" -d "{\"question\":\"介绍项目\"}"
```

应看到内容逐步出现。记录：

- 第一个字符出现需要多久。
- 完整回答需要多久。
- 普通 `/ask` 需要多久。

## 6. 代码填空

### 练习 1：补全会话追加

```python
history.append({"role": ____, "content": question})
```

参考答案：

```python
history.append({"role": "user", "content": question})
```

### 练习 2：补全流式响应

```python
from fastapi.responses import StreamingResponse
return ____(generator(), media_type="text/plain; charset=utf-8")
```

参考答案：

```python
return StreamingResponse(generator(), media_type="text/plain; charset=utf-8")
```

## 7. 常见报错

- 流式仍一次返回：检查是否用了 `StreamingResponse`。
- 历史不生效：检查 `conversation_id` 是否一致。
- 上下文太长：限制历史条数。
- 中文乱码：`media_type` 带 `charset=utf-8`。

## 8. 课后小测

1. 会话记忆保存什么？
2. 流式输出体验好在哪里？
3. 为什么流式接口不能返回普通字典？

## 9. 深度阅读

- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/)
- [LlamaIndex Streaming](https://developers.llamaindex.ai/python/framework/)