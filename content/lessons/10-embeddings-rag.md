# 文本嵌入、向量检索与 RAG

> 本节目标：理解 Embedding、向量数据库、切片、召回和 RAG 的完整流程。

## 一句话理解

Embedding 把文字变成坐标，向量检索负责找最接近的坐标，RAG 则把找到的资料交给模型，让回答更有依据。

## 核心概念

- **Embedding**：把文本映射成向量。
- **向量数据库**：保存和搜索向量。
- **切片**：把长文档拆成较短片段。
- **召回**：从知识库中找出最相关的片段。
- **重排**：在召回结果里再做更精细的排序。
- **RAG**：Retrieval-Augmented Generation，检索增强生成。

打比方：RAG 像开卷考试。模型不是靠记忆硬答，而是先翻到相关资料，再根据资料写答案。

## 必须掌握的代码/命令

```python
# 用一个简单的关键词计数模拟相似度，正式项目通常使用 Embedding 模型。
def score(query, text):
    words = set(query)
    return len(words & set(text))

query = "人工智能"
documents = ["人工智能改变世界", "今天适合跑步", "机器学习是 AI 的分支"]

for doc in documents:
    print(score(query, doc), doc)
```

## 动手任务

把一个长文档切成三段，分别写一句摘要，并判断哪一段最可能被问题召回。

## 课后小测

1. Embedding 为什么适合做语义检索？
2. 切片太大或太小分别有什么问题？
3. RAG 为什么能减少模型凭空回答？

## 深度阅读

- [Datawhale LLM Universe](https://github.com/datawhalechina/llm-universe)
- [Microsoft Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners)