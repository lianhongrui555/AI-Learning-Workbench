# Ollama 本地模型部署与 Python API

> 本节目标：理解 Ollama 的模型管理和 API 调用方式，并用 Python 完成一次本地生成。

## 一句话理解

Ollama 就像你电脑上的模型管家，负责下载、保存、加载和运行本地大模型。你的 Python 程序只要向它发请求，就能拿到生成结果。

## 核心概念

- **模型名称**：例如 `qwen2.5:7b`。
- **拉取模型**：先把模型下载到本机。
- **运行服务**：Ollama 在后台提供 HTTP API。
- **本地端口**：常见端口是 `11434`。
- **提示词**：发送给模型的输入。
- **流式输出**：一边生成一边返回，不必等完整答案。

## 必须掌握的代码/命令

```powershell
# 查看本地模型。
ollama list

# 拉取一个较小的中文对话模型。
ollama pull qwen2.5:1.5b

# 启动命令行对话。
ollama run qwen2.5:1.5b
```

```python
import requests

response = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={"model": "qwen2.5:1.5b", "prompt": "用一句话解释什么是 AI。", "stream": False},
    timeout=120,
)
print(response.json()["response"])
```

## 动手任务

确认 `ollama list` 能看到至少一个模型，再用 Python 发出一次生成请求。

## 课后小测

1. Ollama 在本地 AI 应用里承担什么角色？
2. 为什么本地服务通常使用 `127.0.0.1` 而不是公网地址？
3. 流式输出适合什么场景？

## 深度阅读

- [Ollama 官方文档](https://docs.ollama.com/)
- [Ollama Python Library](https://github.com/ollama/ollama-python)