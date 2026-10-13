"""Flask 对比版本：只保留 health 和最小 ask。"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"framework": "flask", "status": "ok"})


@app.post("/ask")
def ask_api():
    data = request.get_json(silent=True) or {}
    return jsonify({"answer": f"你问的是：{data.get('question', '')}", "sources": [], "latency_ms": 0})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)