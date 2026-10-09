# Agent、工具调用与 CodeHarness

> 本节目标：理解 Agent Loop、工具 Schema、工具执行、观察结果和停止条件。

## 一句话理解

普通模型像只会聊天的顾问，Agent 像可以边想边动手的助手：先决定用什么工具，执行后看看结果，再继续思考，直到任务完成。

## 核心概念

- **Agent**：能循环决策并调用外部能力的模型应用。
- **工具**：文件读取、搜索、计算器、天气接口等。
- **JSON Schema**：告诉模型工具需要哪些参数。
- **观察结果**：工具执行后返回的数据。
- **停止条件**：任务完成、达到最大步数或发生错误。
- **CodeHarness**：一个围绕代码项目构建的本地 Agent 外壳。

## 必须掌握的代码/命令

```python
# 用一个简单工具演示 Agent 可以调用的函数。
def get_weather(city):
    return {"city": city, "temperature": 26, "description": "多云"}

tool_result = get_weather("北京")
print(tool_result)
```

## 代码阅读示例

先不要运行代码，直接阅读并尝试判断它做了什么：

```python
def get_weather(city):
    return {"city": city, "temperature": 26}

print(get_weather("北京"))
```

阅读提示：

- 先找变量分别保存了什么。
- 再追踪每一行执行的顺序。
- 最后判断输出、错误或参数变化。

页面下方有对应的代码理解题，提交后可以查看逐行解释。


## 课后小测

1. Agent 为什么需要工具调用循环？
2. 工具 Schema 不清晰会导致什么问题？
3. 为什么一定要设置最大步数？

## 深度阅读

- [Hugging Face Agents Course](https://github.com/huggingface/agents-course)
- [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners)
- [CodeHarness](https://github.com/lianhongrui555/CodeHarness)