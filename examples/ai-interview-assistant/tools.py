"""面试题工具，不依赖大模型即可测试。"""

import random


QUESTIONS = [
    {"id": 1, "category": "RAG", "difficulty": "基础", "question": "RAG 的完整流程是什么？"},
    {"id": 2, "category": "Agent", "difficulty": "基础", "question": "Agent 为什么需要工具 Schema？"},
    {"id": 3, "category": "Ollama", "difficulty": "基础", "question": "Ollama 默认端口是多少？"},
]


def list_categories() -> list[str]:
    return sorted({item["category"] for item in QUESTIONS})


def pick_question(category: str | None = None) -> dict:
    pool = QUESTIONS if not category else [item for item in QUESTIONS if item["category"] == category]
    return random.choice(pool or QUESTIONS)