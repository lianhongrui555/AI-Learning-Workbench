"""轻量 RAG 评测指标。"""


def safe_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def hit_rate(answer: str, keywords: list[str]) -> float:
    hits = sum(1 for word in keywords if word.lower() in answer.lower())
    return safe_ratio(hits, len(keywords))


def citation_coverage(answer: str, sources: list[str]) -> float:
    return safe_ratio(sum(1 for source in sources if source in answer), len(sources))


def latency_score(latency_ms: int, max_ms: int = 10000) -> float:
    return max(0.0, 1.0 - safe_ratio(latency_ms, max_ms))


def completeness_score(answer: str, min_length: int = 30) -> float:
    return min(1.0, safe_ratio(len(answer), min_length))