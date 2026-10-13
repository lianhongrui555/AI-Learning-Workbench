"""LlamaIndex + Ollama 的本地 RAG 查询封装。"""

import time
from pathlib import Path

from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from settings import settings

Settings.llm = Ollama(model=settings.ollama_model, request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model_name=settings.embed_model)


def build_index() -> None:
    documents = SimpleDirectoryReader(settings.data_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=settings.storage_dir)
    print(f"已索引 {len(documents)} 个文档")


def load_index():
    storage_context = StorageContext.from_defaults(persist_dir=settings.storage_dir)
    return load_index_from_storage(storage_context)


def ask(question: str) -> dict:
    start = time.perf_counter()
    index = load_index()
    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query(question)
    sources = sorted({node.metadata.get("file_name", "unknown") for node in response.source_nodes})
    latency_ms = int((time.perf_counter() - start) * 1000)
    return {"answer": str(response), "sources": sources, "latency_ms": latency_ms}


if __name__ == "__main__":
    if not Path(settings.storage_dir).exists():
        build_index()
    print(ask("项目里有哪些 AI 实践？"))