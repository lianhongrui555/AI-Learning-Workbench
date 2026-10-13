# Ollama 与 Embedding：构建本地知识库

> 本节作品：使用 `qwen2.5:7b` 和 `bge-m3` 构建并持久化本地知识库。
> 预计时间：80～120 分钟。
> 完成标准：索引能用本地 Ollama 重建，并能从 storage 加载。

## 1. 检查 Ollama

```powershell
ollama list
```

必须能看到：

```text
qwen2.5:7b
bge-m3
```

没有就运行：

```powershell
ollama pull qwen2.5:7b
ollama pull bge-m3
```

显存不足时可以把 `qwen2.5:7b` 换成 `qwen2.5:1.5b`。

## 2. 配置本地 LLM

在 `rag.py` 顶部加入：

```python
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(
    model="qwen2.5:7b",
    request_timeout=120.0,
)
```

运行一次 Python，确认没有连接错误。

## 3. 配置本地 Embedding

```python
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.embed_model = OllamaEmbedding(
    model_name="bge-m3",
)
```

这时文档向量和查询向量都由本机生成，不会发送到云端。

## 4. 重建索引

删除旧的 `storage` 后重新构建：

```powershell
Remove-Item storage -Recurse -Force
.\.venv\Scripts\python.exe -X utf8 rag.py
```

> 如果 `storage` 不存在，PowerShell 会提示路径不存在，可以忽略。

应看到重新加载文档并生成 storage。

## 5. 测试重新加载和查询

```python
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
response = query_engine.query("我的项目里做了哪些 AI 实践？")
print(response)
```

观察：

- 回答是否来自资料内容。
- 首次加载是否比重新构建索引快。
- 终端是否显示模型调用耗时。

## 6. 代码填空

### 练习 1：补全 LLM 配置

```python
from llama_index.llms.ollama import Ollama
Settings.llm = Ollama(model=____)
```

参考答案：

```python
Settings.llm = Ollama(model="qwen2.5:7b", request_timeout=120.0)
```

### 练习 2：补全 Embedding 配置

```python
from llama_index.embeddings.ollama import OllamaEmbedding
Settings.embed_model = OllamaEmbedding(model_name=____)
```

参考答案：

```python
Settings.embed_model = OllamaEmbedding(model_name="bge-m3")
```

## 7. 常见报错

- `model not found`：模型没有 pull。
- `Connection refused`：Ollama 未启动。
- `read timeout`：模型太大或首次加载慢，增加 timeout。
- 重建索引后结果异常：确认没有混用不同 Embedding 模型生成的旧索引。

## 8. 课后小测

1. LLM 和 Embedding 模型分别负责什么？
2. 为什么中文知识库要用合适的 Embedding？
3. 持久化索引避免了什么重复工作？

## 9. 深度阅读

- [Ollama 文档](https://docs.ollama.com/)
- [LlamaIndex Ollama 集成](https://developers.llamaindex.ai/python/framework/integrations/llm/ollama/)