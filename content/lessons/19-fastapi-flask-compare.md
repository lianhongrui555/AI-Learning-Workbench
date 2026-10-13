# Flask 与 FastAPI 对比：最小模型 API

> 本节作品：两个能返回 `/health` 的接口。
> 预计时间：70～90 分钟。
> 完成标准：两个接口都能访问，并能说明 FastAPI 的 `/docs` 与 Flask 的差异。

## 1. 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install flask fastapi uvicorn
```

## 2. 写 Flask 版本

新建 `app_flask_compare.py`：

```python
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"framework": "flask", "status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
```

运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 app_flask_compare.py
```

浏览器打开 `http://127.0.0.1:5000/health`，应看到 JSON。

按 `Ctrl + C` 关闭服务。

## 3. 写 FastAPI 版本

新建 `app_fastapi.py`：

```python
from fastapi import FastAPI

app = FastAPI(title="AI Interview Assistant API")


@app.get("/health")
def health():
    return {"framework": "fastapi", "status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
```

运行：

```powershell
.\.venv\Scripts\uvicorn.exe app_fastapi:app --reload --port 8000
```

打开：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

`/docs` 是 FastAPI 自动生成的接口测试页面。

## 4. 对比表

| 对比项 | Flask | FastAPI |
|---|---|---|
| 启动 | `python app.py` | `uvicorn app:app` |
| 自动文档 | 需要扩展 | 默认 `/docs` |
| 数据校验 | 手动或扩展 | 内置 Pydantic |
| 学习曲线 | 非常简单 | 稍多但工程能力更强 |

## 5. 代码填空

### 练习 1：补全 Flask 路由

```python
from flask import Flask, jsonify
app = Flask(__name__)

# 在这里补全 /health 路由
def health():
    return jsonify({"status": "ok"})
```

参考答案：

```python
@app.get("/health")
def health():
    return jsonify({"status": "ok"})
```

### 练习 2：补全 FastAPI 端口

```python
import uvicorn
from app_fastapi import app

uvicorn.run(app, host="127.0.0.1", port=____)
```

参考答案：

```python
uvicorn.run(app, host="127.0.0.1", port=9000)
```

## 6. 常见报错

- `address already in use`：端口被占用，换成 5001 或 8001。
- `uvicorn` 找不到：安装 `uvicorn` 或改用 `python -m uvicorn`。
- `No module named app_fastapi`：确认当前目录和文件名。

## 7. 课后小测

1. FastAPI 的自动文档来自哪里？
2. Flask 和 FastAPI 有哪些共同点？
3. 为什么 host 改成 0.0.0.0 后局域网可能访问？

## 8. 深度阅读

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Flask 官方文档](https://flask.palletsprojects.com/)