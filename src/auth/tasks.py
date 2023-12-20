# from datetime import datetime
#
# from celery import shared_task
# from sqlalchemy import delete
#
# from src.auth.models import BlacklistedToken
# from src.database.engine import sync_session
#
#
# @shared_task(name="remove_expired_tokens")
# def remove_expired_tokens():
#     with sync_session() as session:
#         current_date = datetime.now()
#         session.execute(
#             delete(BlacklistedToken).where(BlacklistedToken.expires_at <= current_date)
#         )
#         session.commit()
#