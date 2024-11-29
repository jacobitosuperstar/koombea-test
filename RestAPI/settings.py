from pydantic_settings import (
    BaseSettings,
)

class Settings(BaseSettings):
    """Application settings.
    ALL the parameters can be configured with environment variables.
    """
    debug: bool = True
    log_level: str = "INFO"
    environment: str = ""
    host: str = "localhost"
    port: int = 8000
    workers_count: int = 1
    rabbit_mq_host: str = "rabbit_mq"
    rabbit_mq_port: str = "5672"

settings: Settings = Settings()
