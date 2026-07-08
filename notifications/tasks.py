from celery import shared_task


@shared_task(bind=True, max_retries=3)
def send_notification(self, message: str) -> bool:
    return True
