# 极简前端与 Docker：完成可演示的 AI 面试助手

> 本节作品：带极简前端、Dockerfile 和演示说明的完整 AI 面试知识库助手。
> 预计时间：90～120 分钟。
> 完成标准：网页能提问并显示答案与引用，容器能启动。

## 1. 创建 templates/index.html

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 面试知识库助手</title>
  <style>
    body { font-family: sans-serif; max-width: 860px; margin: 40px auto; padding: 16px; }
    textarea { width: 100%; height: 100px; }
    pre { background: #f5f5f5; padding: 12px; }
  </style>
</head>
<body>
  <h1>AI 面试知识库助手</h1>
  <textarea id="question" placeholder="输入面试问题"></textarea>
  <button id="ask">提问</button>
  <div id="result"></div>

  <script>
    document.getElementById("ask").addEventListener("click", async () => {
      const question = document.getElementById("question").value.trim();
      if (!question) return;
      const result = document.getElementById("result");
      result.textContent = "正在思考……";
      const response = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();
      result.innerHTML = `<p>${data.answer}</p><pre>${(data.sources || []).join("\\n")}</pre>`;
    });
  </script>
</body>
</html>
```

## 2. 让 FastAPI 返回页面

```powershell
.\.venv\Scripts\python.exe -m pip install jinja2
```

在 `app_fastapi.py` 中：

```python
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

启动：

```powershell
.\.venv\Scripts\uvicorn.exe app_fastapi:app --reload --port 8000
```

打开 `http://127.0.0.1:8000/`，应看到提问页面。

## 3. 测试完整问答

在网页里输入至少 3 个问题：

- 项目有哪些 AI 实践？
- RAG 的流程是什么？
- Agent 的工具调用需要什么？

检查页面是否显示答案和引用。

## 4. 创建 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements-example.txt .

RUN pip install --no-cache-dir -r requirements-example.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
```

创建 `.dockerignore`：

```text
.venv
__pycache__
storage
data/*.db
.env
```

## 5. 构建和运行

```powershell
docker build -t ai-interview-assistant .
docker run -p 8000:8000 ai-interview-assistant
```

浏览器打开 `http://127.0.0.1:8000/`。

如果 Ollama 在 Docker 外，容器内访问要使用：

```text
http://host.docker.internal:11434
```

## 6. 面试演示说明

写一份 3 分钟演示顺序：

1. 打开项目 README，说明项目目标和架构。
2. 展示 `/docs` 中的 API。
3. 在网页中提问并展示引用。
4. 展示评测报告。
5. 说明 Docker 部署和下一步优化。

## 7. 代码填空

### 练习 1：补全前端请求头

```javascript
fetch("/ask", {
  method: "POST",
  headers: {____},
  body: JSON.stringify({question})
})
```

参考答案：

```javascript
headers: {"Content-Type": "application/json"}
```

### 练习 2：补全 Docker 端口

```powershell
docker run -p ____ ai-interview-assistant
```

参考答案：

```powershell
docker run -p 8000:8000 ai-interview-assistant
```

## 8. 常见报错

- 页面空白：检查 JS 控制台和模板路径。
- CORS 或 422：检查请求头、字段名和端口。
- Docker 构建慢：使用国内镜像并减少复制文件。
- 容器访问不到 Ollama：使用 `host.docker.internal`。

## 9. 课后小测

1. 为什么需要最小前端？
2. Dockerfile 的作用是什么？
3. 主机端口和容器端口如何映射？

## 10. 深度阅读

- [FastAPI Templates](https://fastapi.tiangolo.com/advanced/templates/)
- [Docker Get Started](https://docs.docker.com/get-started/)