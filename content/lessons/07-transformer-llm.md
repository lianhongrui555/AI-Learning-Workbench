# Transformer 与大语言模型

> 本节目标：理解注意力机制、Token、上下文窗口、预训练和生成文字的基本过程。

## 一句话理解

大语言模型像一个非常擅长“根据前文猜下一个字”的接龙高手。Transformer 负责让它同时看到前文里哪些词更重要。

## 核心概念

- **Token**：模型处理文字的小块，可能是一个字、一个词或词的一部分。
- **上下文窗口**：模型一次能看到的最大 Token 数量。
- **注意力机制**：动态判断当前应该关注上下文中的哪些部分。
- **预训练**：先让模型从海量文本中学习语言规律。
- **生成**：根据已有内容预测下一个 Token，再不断重复。
- **温度**：控制输出的随机程度。温度越高，回答通常越发散。

打比方：人读句子时会根据前后文理解“它”指谁，注意力机制就是在帮模型完成这件事。

## 必须掌握的代码/命令

```python
# 用简单字典模拟“预测下一个词”。
predictions = {
    "机器": ["学习", "视觉", "智能"],
    "人工": ["智能", "数据", "规则"],
}

print(predictions["机器"])
```

## 动手任务

把一句话拆成 Token，并说明哪些词通常需要结合上下文才能理解。

## 课后小测

1. Token 和普通“字”完全一样吗？
2. 上下文窗口为什么不能无限大？
3. 温度参数通常控制什么？

## 深度阅读

- [Microsoft Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners)
- [Hugging Face Agents Course](https://github.com/huggingface/agents-course)