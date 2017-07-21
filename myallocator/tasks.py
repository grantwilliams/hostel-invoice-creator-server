from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from myallocator.utils import download_bookings, add_to_database

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name='task_download_bookings',
    ignore_result=True
)
def task_download_bookings():
    download_bookings()
    logger.info('Saved bookings spreadsheet')
    task_add_to_database.delay()

@task(name='task_add_to_database')
def task_add_to_database():
    add_to_database()
