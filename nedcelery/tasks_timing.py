
from celery import Celery
from celery.schedules import crontab
from nedcelery.celery import app


# 定义定时任务
app.conf.beat_schedule = {
    'task1': {
        'task': 'users.tasks.add',
        'schedule': 3.0,
        'args': (16, 16)
    },
    'task2': {
        'task': 'users.tasks.multiply',
        'schedule': crontab(minute='*/1'),
        'args': (16, 16)
    },
}
