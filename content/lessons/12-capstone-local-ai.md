# 综合项目：搭建本地 AI 助手

> 本节目标：把模型、API、对话、工具、RAG 和学习工作台组合起来，形成一个可展示的本地 AI 项目。

## 一句话理解

一个小型本地 AI 助手至少包含四层：模型运行层、应用服务层、数据与工具层、用户界面层。每层只负责自己擅长的部分。

## 核心概念

- **模型运行层**：Ollama 负责模型加载和推理。
- **应用服务层**：Flask 接收请求、隐藏 Key、转发到模型服务。
- **数据与工具层**：知识库、天气接口、计算器和文件工具。
- **用户界面层**：网页、桌面应用、小程序或 CLI。
- **最小闭环**：先让“输入 → 模型 → 输出”跑通，再逐步增加工具和知识库。

## 必须掌握的代码/命令

```powershell
# 确认 Ollama 正在运行。
ollama list

# 进入项目目录。
cd D:\Local-AI-Agent\app

# 启动 Flask 服务。
python -X utf8 web_app.py
```

```text
浏览器访问：http://127.0.0.1:5000/
```

## 代码阅读示例

先不要运行代码，直接阅读并尝试判断它做了什么：

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

阅读提示：

- 先找变量分别保存了什么。
- 再追踪每一行执行的顺序。
- 最后判断输出、错误或参数变化。

页面下方有对应的代码理解题，提交后可以查看逐行解释。


## 课后小测

1. 为什么 API Key 不应该放在前端？
2. 最小闭环为什么比一开始堆很多功能更稳？
3. 工具和知识库在一个 AI 助手里分别解决什么问题？

## 深度阅读

- [Local AI Agent](https://github.com/lianhongrui555/Local-AI-Agent)
- [CodeHarness](https://github.com/lianhongrui555/CodeHarness)
- [YOLO Detection](https://github.com/lianhongrui555/YOLO-Detection)