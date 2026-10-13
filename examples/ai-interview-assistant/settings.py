"""应用配置：集中管理端口、模型和路径。"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    ollama_model: str = "qwen2.5:7b"
    embed_model: str = "bge-m3"
    data_dir: str = "data"
    storage_dir: str = "storage"


settings = Settings()