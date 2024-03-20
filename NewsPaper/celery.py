import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# чтобы выполнить какую-то задачу каждый понедельник в 8 утра, необходимо в расписание добавить следующее:
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.weekly_send_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}
