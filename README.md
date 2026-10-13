# AI Learning Workbench

一个面向零基础学习者的本地 AI 学习工作台：课程路线、进度、Markdown 笔记、小测、项目实战和 AI 助教集中在一个网页里。

> **这篇 README 是为电脑小白写的 Windows 本地运行指南。**
>
> 你不需要先安装 Docker、Ollama 或 Dify。课程、进度、笔记、小测和项目卡片都可以先正常使用。
>
> 只有“AI 助教”这个功能需要额外连接本地 Dify；不配置也不会影响其他功能。`n>`n> 课程练习采用代码阅读理解模式：每节 3 道概念题 + 3 道代码题，不需要自己写代码，也不会在工作台中运行代码。

---

# 一、先看整个过程

不用害怕，整个过程只有 7 步：

```text
1. 安装 Python
   ↓
2. 下载 ZIP 压缩包
   ↓
3. 解压到 C 盘
   ↓
4. 用 PowerShell 进入项目目录
   ↓
5. 创建虚拟环境并安装依赖
   ↓
6. 复制并编辑 .env
   ↓
7. 启动工作台并打开浏览器
```

预计第一次需要 10～30 分钟，主要时间会花在下载 Python 和安装依赖上。

---

# 二、运行前必须知道的事

## 1. 这个项目是什么？

这是一个运行在你自己电脑上的学习网页，不是必须联网的在线网站。

启动后浏览器地址通常是：

```text
http://127.0.0.1:5000/
```

`127.0.0.1` 的意思是“这台电脑自己”。所以它不会自动出现在别人电脑上。

## 2. 第一次运行需要联网吗？

需要。

第一次安装 Python 依赖时，电脑要从互联网下载 Flask、requests 等软件包。安装完成后，课程、进度和笔记可以本地使用。

## 3. 需要安装 Docker、Ollama、Dify 吗？

只使用以下功能时，不需要：

- 17 节课程
- 学习进度
- Markdown 笔记
- 概念选择题和代码理解题
- 项目实战卡片

想使用 AI 助教时，才需要另外准备 Dify 和本地 Ollama，或者连接一个可访问的 Dify 服务。

## 4. 路径不要放中文和空格

推荐把项目放在：

```text
C:\AI-Learning-Workbench
```

不建议放在：

```text
C:\Users\某某\桌面\新建文件夹\AI 学习\最终版\
```

虽然 Windows 通常可以处理中文路径，但 Python、PowerShell 和第三方包偶尔会因为特殊路径出现奇怪的编码问题。对小白最稳的做法就是使用简单的英文路径。

---

# 三、第 1 步：安装 Python

## 1. 打开 Python 官网

在浏览器地址栏输入：

```text
https://www.python.org/downloads/windows/
```

或者直接打开：

```text
https://www.python.org/downloads/
```

你会看到一个带黄色按钮的页面，按钮通常写着：

```text
Download Python 3.x.x
```

点击这个按钮。

## 2. 下载 Windows 安装程序

进入下载页面后，找到类似下面的文件：

```text
Windows installer (64-bit)
```

绝大多数 Windows 10/11 电脑选择：

```text
Windows installer (64-bit)
```

如果你的电脑是 ARM 架构，或者不确定，先下载普通的 64-bit 版本。

## 3. 开始安装 Python

双击刚下载的 `.exe` 文件。

安装程序打开后，最重要的一步来了：

> **务必勾选页面底部的 `Add python.exe to PATH`。**

你会看到类似：

```text
[ ] Add python.exe to PATH
```

把它前面的方框打勾。

然后再点击：

```text
Install Now
```

如果弹出“是否允许安装”，点击“是”。

等待安装完成，最后点击：

```text
Close
```

## 4. 验证 Python 是否安装成功

安装完成后，在 Windows 搜索框里输入：

```text
PowerShell
```

点击：

```text
Windows PowerShell
```

会弹出一个深蓝色或黑色窗口。

在窗口里输入：

```powershell
python --version
```

按回车。

正常情况下你会看到类似：

```text
Python 3.12.10
```

再输入：

```powershell
py --version
```

如果也显示 Python 版本，说明安装成功。

### 如果提示“无法将 python 识别为命令”

这通常表示安装时没有勾选 `Add python.exe to PATH`。

解决办法：

1. 重新运行 Python 安装程序。
2. 选择 `Modify` 或重新安装。
3. 确认勾选 `Add python.exe to PATH`。
4. 安装完成后关闭并重新打开 PowerShell。
5. 再次运行 `python --version`。

---

# 四、第 2 步：从 GitHub 下载 ZIP

## 1. 打开项目仓库

浏览器打开：

```text
https://github.com/lianhongrui555/AI-Learning-Workbench
```

你会看到页面顶部有项目名称：

```text
AI-Learning-Workbench
```

页面中间有项目介绍和文件列表。

## 2. 点击绿色 Code 按钮

在文件列表右上方找到绿色的按钮，通常写着：

```text
Code
```

点击它。

### 屏幕上应看到

会弹出一个菜单，里面可能有：

```text
HTTPS
SSH
GitHub CLI
Download ZIP
```

点击最后一项：

```text
Download ZIP
```

浏览器会开始下载一个类似下面的文件：

```text
AI-Learning-Workbench-main.zip
```

默认会保存到：

```text
C:\Users\你的用户名\Downloads
```

## 3. 解压 ZIP

打开“下载”文件夹，找到：

```text
AI-Learning-Workbench-main.zip
```

右键点击它，选择：

```text
全部解压缩...
```

或者：

```text
Extract All...
```

Windows 会让你选择解压位置。

建议解压到：

```text
C:\
```

解压完成后，你可能会得到一个文件夹：

```text
C:\AI-Learning-Workbench-main
```

## 4. 把文件夹改成简单名称

为了后面命令更短，建议把文件夹重命名为：

```text
C:\AI-Learning-Workbench
```

最后你应当得到这样的结构：

```text
C:\AI-Learning-Workbench\
├─ app.py
├─ content\
├─ templates\
├─ static\
├─ scripts\
├─ tests\
├─ requirements.txt
└─ README.md
```

注意：进入这个文件夹后，应该能直接看到 `app.py`。如果外面还套了一层同名文件夹，说明需要再进入一层。

---

# 五、第 3 步：用 PowerShell 进入项目目录

## 1. 打开项目文件夹

打开文件资源管理器，进入：

```text
C:\AI-Learning-Workbench
```

## 2. 在当前位置打开 PowerShell

最简单的方法：

1. 点击文件夹窗口顶部的地址栏。
2. 输入：

```text
powershell
```

3. 按回车。

会弹出一个 PowerShell 窗口。

或者：

1. 在文件夹空白处按住 `Shift`。
2. 点击鼠标右键。
3. 选择“在终端中打开”或“在此处打开 PowerShell 窗口”。

## 3. 确认当前目录正确

在 PowerShell 里输入：

```powershell
Get-Location
```

按回车。

正确结果应该类似：

```text
Path
----
C:\AI-Learning-Workbench
```

如果显示的不是这个目录，就先执行：

```powershell
cd C:\AI-Learning-Workbench
```

再检查一次：

```powershell
Get-Location
```

---

# 六、第 4 步：创建虚拟环境并安装依赖

## 1. 什么是虚拟环境？

可以把虚拟环境理解成“只给这个项目使用的工具箱”。

不同项目需要不同版本的软件包。把依赖装进自己的工具箱里，就不会和别的项目互相打架。

## 2. 创建虚拟环境

在 PowerShell 里输入：

```powershell
python -m venv .venv
```

按回车。

然后等待几秒到几十秒。

成功后，项目目录里会出现一个文件夹：

```text
.venv
```

### 屏幕上应看到

PowerShell 通常不会输出任何内容。没有红字报错就是成功。

你可以输入：

```powershell
Get-ChildItem -Force
```

应该能看到：

```text
.venv
app.py
content
templates
...
```

## 3. 升级 pip

继续输入：

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

按回车。

你会看到下载和安装过程，最后通常会出现：

```text
Successfully installed pip-...
```

## 4. 安装项目依赖

输入：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

按回车。

第一次会下载 Flask、requests、python-dotenv 和 pytest。

### 屏幕上应看到

最后大致会出现：

```text
Successfully installed Flask-... requests-... python-dotenv-... pytest-...
```

### 如果下载很慢

可以使用国内镜像：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 如果提示“找不到 Python”

回到第 1 步，确认 Python 安装成功，并且 `python --version` 能显示版本。

### 如果提示虚拟环境不存在

说明 `.venv` 没有创建成功。重新执行：

```powershell
python -m venv .venv
```

然后再安装依赖。

---

# 七、第 5 步：复制并配置 .env

## 1. 什么是 .env？

`.env` 是项目的“私人设置文件”。

它负责保存：

- 网页监听地址
- 网页端口
- 数据库路径
- AI 助教地址
- AI 助教 API Key

真实 API Key 只能放在这个文件里，不能提交到 GitHub。

## 2. 复制配置模板

在 PowerShell 里执行：

```powershell
Copy-Item .env.example .env
```

执行成功后通常没有提示。

输入：

```powershell
Get-ChildItem -Force
```

应该能看到：

```text
.env
.env.example
```

## 3. 用记事本打开 .env

输入：

```powershell
notepad .env
```

会打开记事本。

你会看到类似内容：

```text
WEB_HOST=127.0.0.1
WEB_PORT=5000
DATABASE_PATH=
DIFY_TUTOR_API_URL=http://localhost/v1/chat-messages
DIFY_TUTOR_API_KEY=请在这里粘贴学习助教API密钥
```

## 4. 只使用基础功能时怎么填？

如果你只想先使用课程、进度、笔记、小测和项目卡片，可以保持：

```text
WEB_HOST=127.0.0.1
WEB_PORT=5000
DATABASE_PATH=
```

`DIFY_TUTOR_API_KEY` 可以暂时保留占位文字。

这样启动后除了 AI 助教，其他功能都能使用。

## 5. 使用 AI 助教时怎么填？

你必须先有自己的 Dify 服务，并创建一个专用聊天应用。

然后在 `.env` 中填写：

```text
DIFY_TUTOR_API_URL=http://localhost/v1/chat-messages
DIFY_TUTOR_API_KEY=你的真实APIKey
```

如果 Dify 运行在另一台局域网电脑上，地址要改成类似：

```text
DIFY_TUTOR_API_URL=http://192.168.1.10/v1/chat-messages
```

把 `192.168.1.10` 替换成实际 Dify 服务器地址。

## 6. 保存 .env

在记事本里按：

```text
Ctrl + S
```

保存后关闭记事本。

### 重要安全提醒

不要：

- 把 `.env` 发给别人
- 把 API Key 截图发到群里
- 把 `.env` 上传到 GitHub
- 把密钥直接写进 `app.py`

项目已经通过 `.gitignore` 忽略 `.env`。

---

# 八、第 6 步：启动工作台

## 1. 确认你在项目根目录

PowerShell 中执行：

```powershell
Get-Location
```

应该是：

```text
C:\AI-Learning-Workbench
```

## 2. 启动 Flask 服务

输入：

```powershell
.\.venv\Scripts\python.exe -X utf8 app.py
```

按回车。

### 屏幕上应看到

正常情况下会显示类似：

```text
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

这表示工作台已经启动成功。

> 这个 PowerShell 窗口要保留，不要关闭。
>
> 关闭窗口后，网页服务也会停止。

## 3. 打开浏览器

打开 Chrome、Edge 或其他浏览器，在地址栏输入：

```text
http://127.0.0.1:5000/
```

按回车。

### 你应该看到

一个深色终端风的页面，左侧有：

```text
01 总览
02 学习路线
03 项目实战
04 笔记库
05 AI 助教
```

页面顶部会显示：

```text
零基础 AI 学习工作台
```

如果看到这些内容，说明运行成功。

## 4. 停止工作台

在运行 Flask 的 PowerShell 窗口里按：

```text
Ctrl + C
```

Windows 可能会问“是否终止批处理操作”，输入：

```text
Y
```

然后按回车。

也可以直接关闭那个 PowerShell 窗口。

---

# 九、第 7 步：以后如何快速启动

## 方法一：每次用命令启动

打开项目目录的 PowerShell，执行：

```powershell
.\.venv\Scripts\python.exe -X utf8 app.py
```

然后打开：

```text
http://127.0.0.1:5000/
```

## 方法二：使用一键启动脚本

项目里已经包含：

```text
scripts\start_workbench.ps1
```

在 PowerShell 中执行：

```powershell
.\scripts\start_workbench.ps1
```

脚本会自动：

1. 检查工作台是否已经运行。
2. 如果没有运行，就在后台启动。
3. 等待服务准备好。
4. 自动打开浏览器。

### 如果 PowerShell 拒绝运行脚本

在 PowerShell 中先执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

然后再次执行：

```powershell
.\scripts\start_workbench.ps1
```

`-Scope Process` 只影响当前这个 PowerShell 窗口，不会永久修改电脑设置。

## 方法三：创建桌面快捷方式

在 PowerShell 中运行下面的命令，可以把启动脚本固定成桌面快捷方式：

```powershell
$ws = New-Object -ComObject WScript.Shell
$shortcut = $ws.CreateShortcut("$env:USERPROFILE\Desktop\AI学习工作台.lnk")
$shortcut.TargetPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$shortcut.Arguments = '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\AI-Learning-Workbench\scripts\start_workbench.ps1"'
$shortcut.WorkingDirectory = "C:\AI-Learning-Workbench"
$shortcut.Save()
```

如果你的项目路径不是 `C:\AI-Learning-Workbench`，要把命令里的路径改成实际路径。

---

# 十、每个页面能做什么

## 01 总览

显示：

- 已完成课程数
- 总进度条
- 下一节推荐课程
- 项目实战状态

## 02 学习路线

显示 5 个阶段、17 节课程：

1. 什么是 AI、机器学习和生成式 AI
2. 数据、特征、标签、训练与推理
3. Python 与 AI 开发工具链
4. 向量、相似度与概率直觉
5. 经典机器学习
6. 神经网络与深度学习
7. Transformer 与大语言模型
8. Prompt 工程与多轮对话
9. Ollama 本地模型部署与 Python API
10. 文本嵌入、向量检索与 RAG
11. Agent、工具调用与 CodeHarness
12. 综合项目：搭建本地 AI 助手
13. 目标检测与 YOLO 入门
14. 数据集、标注与训练/验证划分
15. YOLO 训练实战：从配置到 best.pt
16. 模型评估与调参：Precision、Recall、mAP
17. YOLO 推理与 Flask 摄像头部署

## 03 项目实战

包含三个项目入口：

- Local-AI-Agent
- CodeHarness
- YOLO-Detection

可以标记“已完成/未完成”。

## 04 笔记库

集中显示每节课的笔记。笔记保存在本地 SQLite，不上传 GitHub。

## 05 AI 助教

可以选择当前课程，然后提问。助教会自动带上课程标题和摘要。

AI 助教需要 Dify 和 Ollama。没有配置时，其他功能不受影响。

---

# 十一、常见问题与解决方法

## 问题 1：python 不是内部或外部命令

原因：Python 没有加入 PATH。

解决：

1. 重新运行 Python 安装程序。
2. 勾选 `Add python.exe to PATH`。
3. 重新打开 PowerShell。
4. 再次运行 `python --version`。

## 问题 2：Activate.ps1 无法加载

如果使用激活脚本时被 PowerShell 拦截，可以改用不激活的方式：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 app.py
```

本项目推荐直接使用 `.venv\Scripts\python.exe`，不需要激活虚拟环境。

## 问题 3：pip 下载很慢或超时

使用国内镜像：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 问题 4：端口 5000 被占用

打开 `.env`，改成：

```text
WEB_PORT=5001
```

重新启动后访问：

```text
http://127.0.0.1:5001/
```

## 问题 5：页面无法打开

依次检查：

1. 运行 Flask 的 PowerShell 窗口是否还开着。
2. 窗口里有没有红色错误。
3. 浏览器地址是不是 `http://127.0.0.1:5000/`。
4. 端口是否和 `.env` 中的 `WEB_PORT` 一致。
5. 是否杀毒软件或防火墙拦截了 Python。

## 问题 6：AI 助教返回 503

可能原因：

- `.env` 中的 `DIFY_TUTOR_API_KEY` 没有填写。
- Dify 没有启动。
- `DIFY_TUTOR_API_URL` 地址不正确。
- Dify 所在电脑没有开放对应端口。

如果暂时不修助教，课程、进度、笔记、小测和项目卡片仍然可以正常使用。

## 问题 7：页面显示“数据库无法打开”或数据表错误

检查 `.env`：

```text
DATABASE_PATH=
```

留空表示自动使用项目里的：

```text
data\workbench.db
```

确认 `data` 文件夹存在，并且当前用户有写入权限。

## 问题 8：想重新开始所有进度怎么办？

先关闭 Flask，然后删除：

```text
data\workbench.db
```

再次启动后，工作台会创建新的空数据库。

> 删除数据库会同时清空进度、笔记、小测分数和项目状态，操作前请确认。

---

# 十二、如何更新到最新版

## 方法一：重新下载 ZIP

这是小白最稳妥的方法：

1. 打开 GitHub 仓库。
2. 点击 `Code`。
3. 点击 `Download ZIP`。
4. 解压新版本。
5. 保留原来的 `data\workbench.db`，把它复制到新目录。
6. 重新安装依赖并启动。

## 方法二：使用 Git

如果你已经会用 Git：

```powershell
git pull
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

然后重新启动。

---

# 十三、项目结构

```text
AI-Learning-Workbench/
├─ app.py                     # Flask 后端
├─ content_loader.py          # 课程加载和 Markdown 渲染
├─ content/
│  ├─ curriculum.json         # 17 节课程元数据和小测
│  ├─ projects.json           # 项目实战卡片
│  └─ lessons/                # 17 节 Markdown 正文
├─ templates/                 # 页面模板
├─ static/                    # 深色终端风 CSS 和 JavaScript
├─ data/                      # 本地 SQLite 数据，不提交
├─ tests/                     # 自动化测试
├─ scripts/
│  ├─ check_content.py        # 课程完整性检查
│  └─ start_workbench.ps1     # Windows 一键启动
├─ dify/
│  ├─ README.md               # Dify 助教配置说明
│  └─ system-prompt.md        # 助教系统提示词
├─ requirements.txt
└─ README.md
```

---

# 十四、开发者信息

## 运行测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 检查课程内容

```powershell
.\.venv\Scripts\python.exe scripts\check_content.py
```

## 技术栈

- Python 3.10+
- Flask
- SQLite
- requests
- python-dotenv
- 原生 HTML/CSS/JavaScript

## 内容策略

本项目采用“本地精简导学正文 + 外部深度阅读链接”的混合模式：

- 本地保存学习目标、核心概念、代码阅读示例、3 道概念题和 3 道代码理解题。\n- 工作台不执行代码，也不要求用户自己编写代码。
- 长篇理论、官方文档和视频通过外部链接访问。
- 不复制没有明确许可证的第三方源码。
- 引用信息记录在 `THIRD_PARTY_NOTICES.md`。

## 许可证

MIT License。

---

# 十五、最短操作清单

如果你已经完成 Python 安装，只想快速启动，按下面执行：

```powershell
cd C:\AI-Learning-Workbench

python -m venv .venv

.\.venv\Scripts\python.exe -m pip install --upgrade pip

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Copy-Item .env.example .env

notepad .env

.\.venv\Scripts\python.exe -X utf8 app.py
```

浏览器打开：

```text
http://127.0.0.1:5000/
```

完成。