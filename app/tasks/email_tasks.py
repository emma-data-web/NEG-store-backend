import asyncio

from celery_app import celery
from app.core.email import send_verification_email, send_reset_password_email


@celery.task
def send_verification_email_task(
    recipient_email: str,
    verification_link: str,
):
    asyncio.run(
        send_verification_email(
            recipient_email,
            verification_link,
        )
    )



@celery.task
def send_reset_password_email_task(
    recipient_email: str,
    verification_link: str
):
    asyncio.run(
        send_reset_password_email(
            recipient_email,
            verification_link, 
        )
    )
