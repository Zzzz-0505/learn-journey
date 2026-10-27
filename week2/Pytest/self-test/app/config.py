from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    log_level:str = "INFO"
    debug:bool = False
    max_title_length:int = 20
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

settings = Settings()