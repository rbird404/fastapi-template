from celery import Celery

from src.config import settings

app: Celery = Celery(
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Register apps tasks
# app.autodiscover_tasks(
#     ['src.auth']
# )
