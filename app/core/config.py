from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  JWT_ALGORITHM: str
  ACESS_TOKEN_EXPIRE_MINUTE: int = 30
  EMAIL_USER: str
  EMAIL_PASSWORD: str

  class config:
     env_file = "dev.env"

Settings = Settings()