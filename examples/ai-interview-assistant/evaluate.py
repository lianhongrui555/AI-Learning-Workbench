"""调用 /ask 接口并输出简单评测报告。"""

import csv
import json
from pathlib import Path

import requests

from metrics import citation_coverage, completeness_score, hit_rate, latency_score

questions = json.loads(Path("data/eval_questions.json").read_text(encoding="utf-8"))
rows = []
for item in questions:
    response = requests.post("http://127.0.0.1:8000/ask", json={"question": item["question"]}, timeout=120)
    data = response.json()
    rows.append({
        "question": item["question"],
        "hit_rate": hit_rate(data.get("answer", ""), item.get("keywords", [])),
        "citation_coverage": citation_coverage(data.get("answer", ""), data.get("sources", [])),
        "latency_score": latency_score(data.get("latency_ms", 99999)),
        "completeness": completeness_score(data.get("answer", "")),
    })

with Path("evaluation_report.csv").open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
print("评测完成")