# Pydantic 配置与错误处理

> 本节作品：`settings.py`、`models.py` 和统一错误响应。
> 预计时间：70～90 分钟。
> 完成标准：合法请求通过，非法请求返回结构化错误。

## 1. 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install pydantic pydantic-settings fastapi uvicorn
```

## 2. 创建 settings.py

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    model: str = "qwen2.5:7b"
    embed_model: str = "bge-m3"


settings = Settings()
```

运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "from settings import settings; print(settings)"
```

应看到一个配置对象。

## 3. 创建 .env.example

```text
APP_HOST=127.0.0.1
APP_PORT=8000
OLLAMA_MODEL=qwen2.5:7b
EMBED_MODEL=bge-m3
```

复制：

```powershell
Copy-Item .env.example .env
```

`.env` 是本地配置，不要上传 Git。

## 4. 创建 models.py

```python
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    conversation_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = []
    latency_ms: int = 0
```

测试：

```powershell
.\.venv\Scripts\python.exe -X utf8 -c "from models import AskRequest; print(AskRequest(question='什么是RAG'))"
```

## 5. 接入 FastAPI

在 `app_fastapi.py` 中增加：

```python
from fastapi import FastAPI
from models import AskRequest, AskResponse

app = FastAPI(title="AI Interview Assistant API")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return AskResponse(answer=f"你问的是：{request.question}", sources=[], latency_ms=0)
```

运行：

```powershell
.\.venv\Scripts\uvicorn.exe app_fastapi:app --reload --port 8000
```

## 6. 测试合法和非法请求

合法：

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType application/json -Body '{"question":"什么是RAG"}'
```

非法：

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method Post -ContentType application/json -Body '{}'
```

非法请求应收到 422 和字段说明。

## 7. 统一错误处理器

```python
from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "detail": str(exc)},
    )
```

真实部署时不要在 `detail` 中暴露数据库密码等敏感信息。

## 8. 代码填空

### 练习 1：补全配置字段

```python
class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    # 增加 model 字段，默认 qwen2.5:7b
```

参考答案：

```python
model: str = "qwen2.5:7b"
```

### 练习 2：补全请求模型

```python
class AskRequest(BaseModel):
    # 增加 question 字符串字段
    pass
```

参考答案：

```python
question: str
```

## 9. 常见报错

- 422：请求字段不符合模型。
- `ImportError: pydantic_settings`：未安装 `pydantic-settings`。
- 500：查看终端堆栈。
- 字段类型错误：检查前端和模型字段类型是否一致。

## 10. 课后小测

1. Pydantic 校验解决了什么问题？
2. 422 和 500 分别代表什么？
3. 为什么配置和密钥不要散落在业务代码里？

## 11. 深度阅读

- [Pydantic 文档](https://docs.pydantic.dev/)
- [FastAPI 错误处理](https://fastapi.tiangolo.com/tutorial/handling-errors/)