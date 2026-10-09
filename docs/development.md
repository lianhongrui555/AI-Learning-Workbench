# 开发说明

## 运行

```powershell
python -X utf8 app.py
```

默认监听 `127.0.0.1:5000`，可以通过 `.env` 修改。

## 后端分层

- `content_loader.py`：读取课程 JSON 和 Markdown，并生成安全 HTML。
- `app.py`：Flask 路由、SQLite 数据和 Dify 助教代理。
- `templates/`：页面结构。
- `static/`：终端风 CSS 和原生 JavaScript。

## 数据表

- `lesson_progress`：课程完成状态和分数。
- `notes`：Markdown 笔记。
- `project_progress`：项目实战完成状态。
- `tutor_conversations`：每节课的 Dify 对话编号。
- `tutor_messages`：本地助教消息记录。

## 新增课程

1. 在 `content/lessons/` 新增 Markdown 文件。
2. 在 `content/curriculum.json` 增加课程元数据和 3 道小测。
3. 运行 `python scripts/check_content.py`。
4. 运行 `python -m unittest discover -s tests -v`。