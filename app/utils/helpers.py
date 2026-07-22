from fastapi_mail import ConnectionConfig
from app.core.config import Settings

conf = ConnectionConfig(
    MAIL_USERNAME=Settings.MAIL_USERNAME,
    MAIL_PASSWORD=Settings.MAIL_PASSWORD,
    MAIL_FROM=Settings.MAIL_FROM,
    MAIL_PORT=Settings.MAIL_PORT,
    MAIL_SERVER=Settings.MAIL_SERVER,
    MAIL_STARTTLS=Settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=Settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=Settings.USE_CREDENTIALS,
    VALIDATE_CERTS=Settings.VALIDATE_CERTS,
)

