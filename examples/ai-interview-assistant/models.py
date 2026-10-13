"""FastAPI 请求和响应模型。"""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    conversation_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = []
    latency_ms: int = 0


class AgentRequest(BaseModel):
    task: str