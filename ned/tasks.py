
from ned.celery import instance
# from celery.schedules import crontab
import time


# 异步任务定义
@instance.task
def add(x, y):
    for i in range(3):
        time.sleep(1)
    return x + y


@instance.task(bind=True)
def add_result(self, x, y):
    for i in range(2):
        time.sleep(1)

    return {'x': x, 'y': y, 'x+y': x+y}


# 定时任务定义
# instance.conf.beat_schedule = {
#     'task1': {
#         'task': 'users.tasks.add',
#         'schedule': 3.0,
#         'args': (16, 16)
#     },
#     'task2': {
#         'task': 'users.tasks.multiply',
#         'schedule': crontab(minute='*/1'),
#         'args': (16, 16)
#     },
# }
