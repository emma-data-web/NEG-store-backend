from celery import Celery


celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
)



celery.conf.imports = (
    "app.tasks.email_tasks"
)