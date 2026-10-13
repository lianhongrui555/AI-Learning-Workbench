# AI 面试知识库助手

这是 AI-Learning-Workbench 第 18～27 节的连续参考项目。

## 运行顺序

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull qwen2.5:7b
ollama pull bge-m3
.\.venv\Scripts\python.exe -X utf8 rag.py
.\.venv\Scripts\uvicorn.exe app_fastapi:app --reload --port 8000
```

打开 `http://127.0.0.1:8000/`。