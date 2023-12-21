from celery import Celery

from src.config import settings
from src.auth.tasks import task_settings as auth_task_settings

app: Celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

app.autodiscover_tasks(
    ['src.auth']
)

app.conf.beat_schedule = {
    **auth_task_settings
}
