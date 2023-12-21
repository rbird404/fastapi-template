from datetime import datetime, timedelta

from sqlalchemy import delete
from celery import shared_task

from src.auth.models import BlacklistedToken
from src.database.engine import sync_session


@shared_task
def remove_expired_tokens():
    with sync_session() as session:
        current_date = datetime.now()
        session.execute(
            delete(BlacklistedToken).where(BlacklistedToken.expires_at <= current_date)
        )
        session.commit()


task_settings = {
    'remove-expired-tokens-every-week': {
        'task': 'src.auth.tasks.remove_expired_tokens',
        'schedule': timedelta(weeks=1),
    }
}
