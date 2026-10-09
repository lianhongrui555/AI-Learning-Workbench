# Dify AI 学习助教配置

1. 在 Dify 新建一个聊天应用。
2. 名称填写 `AI学习助教`。
3. 模型选择本地 Ollama 模型，例如 `qwen2.5:7b`。
4. 将 `system-prompt.md` 中的内容粘贴到系统提示词。
5. 打开 API 访问页面，创建应用 API Key。
6. 在项目 `.env` 中填写：

```text
DIFY_TUTOR_API_URL=http://localhost/v1/chat-messages
DIFY_TUTOR_API_KEY=你的学习助教APIKey
```

Flask 会把当前课程标题和摘要拼进每次提问，因此同一个 Dify 应用可以服务全部课程。