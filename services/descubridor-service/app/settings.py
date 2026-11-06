from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    pishop_app_env: str = "dev"
    pishop_service_name: str = "descubridor-service"
    pishop_http_port: int = 8090
    pishop_consul_url: str = "http://consul:8500"  # <-- Cambiado de localhost a consul

    model_config = SettingsConfigDict(
        env_prefix="PISHOP_",
        env_file=".env",
        extra="ignore"
    )

settings = Settings()