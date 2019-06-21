
from celery import Celery
from celery.schedules import crontab
from app import app
import time
from importlib import import_module, reload

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_URL = 'amqp://user:password@rabbitmq:5672/my_vhost'

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@127.0.0.1:5672/'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.conf.CELERY_IMPORTS = ['task', 'task.all_task']
celery.conf.update(app.config)


# tell celery where to find the tasks
# celery.autodiscover_tasks()

#
# # 异步任务定义
# @celery.task
# def add(x, y):
#     for i in range(3):
#         time.sleep(1)
#     return x + y
#
#
# @celery.task(bind=True)
# def add_result(self, x, y):
#     for i in range(2):
#         time.sleep(1)
#
#     return {'x': x, 'y': y, 'x+y': x+y}
#
#
# 定时任务定义
# celery.conf.beat_schedule = {
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


# CELERYD_MAX_TASKS_PER_CHILD = 10

# celery -A nedcelery.celery beat -l INFO
# celery -A nedcelery.celery worker -l INFO
# celery -A nedcelery.celery worker -b -l info

def import_string(import_name):
    import_name = str(import_name).replace(':', '.')
    modules = import_name.split('.')
    mod = import_module(modules[0])
    for comp in modules[1:]:
        if not hasattr(mod, comp):
            reload(mod)
        mod = getattr(mod, comp)
    return mod


@celery.task
def execute(func, *args, **kwargs):
    func = import_string(func)
    return func(*args, **kwargs)