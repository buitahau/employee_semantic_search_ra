from pydantic_settings import BaseSettings


class SourceDBConfig(BaseSettings):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str

    class Config:
        env_prefix = "SOURCE_DB_"


class VectorDBConfig(BaseSettings):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str

    class Config:
        env_prefix = "VECTOR_DB_"


class Settings(BaseSettings):
    source_db: SourceDBConfig = SourceDBConfig()
    vector_db: VectorDBConfig = VectorDBConfig()
    openai_api_key: str
    embedding_model_path: str = "models/all-MiniLM-L6-v2.onnx"
    embedding_service_url: str | None = None


settings = Settings()
