"""FastAPI 主应用。"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from models import AgentRequest, AskRequest, AskResponse
from settings import settings
from tools import pick_question

app = FastAPI(title="AI Interview Assistant API")
templates = Jinja2Templates(directory="templates")


@app.get("/health")
def health():
    return {"status": "ok", "model": settings.ollama_model}


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask", response_model=AskResponse)
def ask_api(request: AskRequest):
    return AskResponse(answer=f"你问的是：{request.question}", sources=[], latency_ms=0)


@app.post("/agent")
def agent_api(request: AgentRequest):
    return {"task": request.task, "tool": "pick_question", "result": pick_question()}


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal_error", "detail": str(exc)})