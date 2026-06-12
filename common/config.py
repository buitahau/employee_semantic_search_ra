from pydantic_settings import BaseSettings, SettingsConfigDict


class SourceDBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SOURCE_DB_", env_file=".env", extra="ignore")

    host: str
    port: int = 5432
    name: str
    user: str
    password: str


class VectorDBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VECTOR_DB_", env_file=".env", extra="ignore")

    host: str
    port: int = 5432
    name: str
    user: str
    password: str


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LLM_", env_file=".env", extra="ignore")

    api_key:  str = ""
    base_url: str = "https://lightning.ai/api/v1"
    model:    str = "openai/gpt-4.1-mini"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    source_db: SourceDBConfig = SourceDBConfig()
    vector_db: VectorDBConfig = VectorDBConfig()
    llm: LLMConfig = LLMConfig()
    openai_api_key: str = ""
    embedding_model_path: str = "models/all-MiniLM-L6-v2.onnx"
    embedding_service_url: str | None = None


settings = Settings()
