from pydantic_settings import BaseSettings

class settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  JWT_ALGORITHMS: str
  ACESS_TOKEN_EXPIRE_MINUTE: int = 30
  EMAIL_USER: str
  EMAIL_PASSWORD: str


Settings = settings()