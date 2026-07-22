from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  JWT_ALGORITHM: str
  ACESS_TOKEN_EXPIRE_MINUTE: int = 30
  #SENDER_EMAIL : str
  #SENDGRID_API_KEY: str
  EMAIL_VERIFY_URL: str
  EMAIL_RESET_LINK: str
  RESET_PASSWORD_TOKEN_EXPIRE_MINUTE: int =  5
  MAIL_USERNAME : str
  MAIL_PASSWORD: str
  MAIL_FROM: str
  MAIL_PORT: int
  MAIL_SERVER: str
  MAIL_STARTTLS: bool
  MAIL_SSL_TLS: bool
  USE_CREDENTIALS: bool
  VALIDATE_CERTS: bool

  class Config:
     env_file = "dev.env"

Settings = Settings()



