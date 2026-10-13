# LlamaIndex 入门：加载、切片与索引

> 本节作品：`rag.py` 能加载 `data` 目录并生成持久化索引。
> 预计时间：80～110 分钟。
> 完成标准：`storage` 目录生成，重新加载索引成功。

## 1. 安装 LlamaIndex

```powershell
.\.venv\Scripts\python.exe -m pip install llama-index-core llama-index-llms-ollama llama-index-embeddings-ollama
```

## 2. 准备资料

```powershell
mkdir data
Get-ChildItem data
```

把 3～5 个 Markdown 或 txt 文件复制到 `data`。

## 3. 加载文档

新建 `rag.py`：

```python
from llama_index.core import SimpleDirectoryReader


def load_documents():
    documents = SimpleDirectoryReader("data").load_data()
    print("文档数量:", len(documents))
    return documents


if __name__ == "__main__":
    load_documents()
```

运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 rag.py
```

应看到文档数量大于 0。

## 4. 切片并构建索引

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex


def build_index():
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir="storage")
    print("索引已保存到 storage")
    return index


if __name__ == "__main__":
    build_index()
```

运行后会生成 `storage` 目录。

## 5. 重新加载索引

```python
from llama_index.core import StorageContext, load_index_from_storage


def load_index():
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)
    print("索引加载成功")
    return index


if __name__ == "__main__":
    load_index()
```

## 6. 代码填空

### 练习 1：补全目录加载

```python
documents = SimpleDirectoryReader(____).load_data()
```

参考答案：

```python
documents = SimpleDirectoryReader("data").load_data()
```

### 练习 2：补全索引创建

```python
index = VectorStoreIndex.____(documents)
```

参考答案：

```python
index = VectorStoreIndex.from_documents(documents)
```

## 7. 常见报错

- `No module named llama_index`：装到错误 Python。
- `FileNotFoundError: data`：当前目录没有 data。
- 下载模型超时：先用默认模型跑通，下一节配置本地 Ollama。
- 空索引：data 中没有可读文本。

## 8. 课后小测

1. SimpleDirectoryReader 的作用是什么？
2. 为什么长文档要切片？
3. 持久化索引有什么好处？

## 9. 深度阅读

- [LlamaIndex Framework 文档](https://developers.llamaindex.ai/python/framework/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)