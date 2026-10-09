# Python 与 AI 开发工具链

> 本节目标：知道 Python、虚拟环境、包管理、Git、终端和 GPU 驱动各自负责什么。

## 一句话理解

Python 是工作语言，虚拟环境是独立工具箱，pip 是装工具的仓库，Git 是项目的时间机器，终端是发命令的遥控器，GPU 驱动是显卡和程序之间的翻译官。

## 核心概念

- **Python**：AI 代码和脚本最常用的语言。
- **虚拟环境**：为每个项目创建独立的依赖空间，避免版本互相打架。
- **pip**：安装 Python 包。
- **Git**：保存版本、比较修改、回退历史和协作。
- **终端**：通过文字命令执行程序。
- **CUDA/驱动**：让需要 GPU 的模型使用显卡。

## 必须掌握的代码/命令

```powershell
# 创建虚拟环境。
python -m venv .venv

# 激活虚拟环境。
.\.venv\Scripts\Activate.ps1

# 升级 pip 并安装依赖。
python -m pip install --upgrade pip
pip install -r requirements.txt
```

```powershell
# 检查 Git 当前状态。
git status
```

## 动手任务

打开一个空文件夹，创建虚拟环境并运行：

```python
print("环境准备完成")
```

## 课后小测

1. 为什么不同项目最好不要共用同一个依赖环境？
2. pip 和 Python 解释器分别负责什么？
3. Git 的“提交”可以理解成什么？

## 深度阅读

- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
- [Datawhale LLM Universe](https://github.com/datawhalechina/llm-universe)