import asyncio

from celery_app import celery
from app.core.email import send_verification_email


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