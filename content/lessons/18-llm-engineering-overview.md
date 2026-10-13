# LLM 应用工程全景：建立项目骨架

> 本节作品：一个能检查 Python、目录、依赖和 Ollama 状态的 `check_env.py`。
> 预计时间：60～90 分钟。
> 完成标准：脚本能在 PowerShell 中正常运行，并输出 OK/FAIL 结果。

## 1. 开始前先检查电脑

按下 `Win + R`，输入 `powershell`，按回车。

输入：

```powershell
python --version
```

必须看到类似 `Python 3.12.10`。如果提示找不到 python，先完成 Python 安装。

## 2. 创建项目文件夹

推荐路径：

```text
D:\ai-interview-assistant
```

在 PowerShell 中逐行执行：

```powershell
D:
mkdir ai-interview-assistant
cd ai-interview-assistant
Get-Location
```

应看到：

```text
D:\ai-interview-assistant
```

## 3. 创建虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe --version
```

应输出版本号。不要直接双击 Python 文件运行，本课程统一使用 `.venv\Scripts\python.exe`。

## 4. 安装基础依赖

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install requests python-dotenv fastapi uvicorn
```

下载慢时加：

```powershell
-i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 5. 跟写 check_env.py

新建 `check_env.py`：

```python
from pathlib import Path


def check_folder():
    current = Path.cwd().name
    if current == "ai-interview-assistant":
        print("目录检查: OK")
    else:
        print(f"目录检查: FAIL，当前目录是 {current}")


if __name__ == "__main__":
    check_folder()
```

运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 check_env.py
```

应看到 `目录检查: OK`。

然后把文件升级成完整版本：

```python
import sys
from pathlib import Path

import requests


def check_folder():
    current = Path.cwd().name
    print("目录检查:", "OK" if current == "ai-interview-assistant" else f"FAIL: {current}")


def check_python():
    version = sys.version.split()[0]
    print("Python 版本:", version)
    print("Python 检查:", "OK" if sys.version_info >= (3, 10) else "FAIL")


def check_ollama():
    try:
        response = requests.get("http://127.0.0.1:11434/api/version", timeout=3)
        print("Ollama 检查:", "OK" if response.status_code == 200 else "FAIL")
    except requests.RequestException:
        print("Ollama 检查: FAIL，请先启动 Ollama")


if __name__ == "__main__":
    check_folder()
    check_python()
    check_ollama()
```

## 6. 正常输出与常见报错

正常输出类似：

```text
目录检查: OK
Python 版本: 3.12.10
Python 检查: OK
Ollama 检查: OK
```

常见问题：

- `No module named requests`：依赖装错环境。
- `Ollama 检查: FAIL`：Ollama 没有启动。
- `目录检查: FAIL`：PowerShell 不在项目目录。

修复命令：

```powershell
.\.venv\Scripts\python.exe -m pip install requests
cd D:\ai-interview-assistant
ollama list
```

## 7. 代码填空

### 练习 1：补全版本输出

```python
import sys

def check_python():
    # 打印 Python 版本
    pass
```

参考答案：

```python
import sys

def check_python():
    print("Python", sys.version.split()[0])
```

解释：`sys.version` 是完整版本文本，`split()[0]` 取第一段。

### 练习 2：补全目录判断

```python
from pathlib import Path

def check_folder():
    current = Path.cwd().name
    # 判断 current 是否等于 ai-interview-assistant
    pass
```

参考答案：

```python
from pathlib import Path

def check_folder():
    current = Path.cwd().name
    print("OK" if current == "ai-interview-assistant" else "FAIL")
```

## 8. 课后小测

1. 为什么 Web API、模型层和检索层应该分开？
2. 虚拟环境解决什么问题？
3. 为什么先跑通最小闭环再增加功能？

## 9. 深度阅读

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [LlamaIndex Framework](https://developers.llamaindex.ai/python/framework/)
- [Ollama 文档](https://docs.ollama.com/)