
from .config import celery_app
import time


## 异步任务定义

@celery_app.task
def add(x, y):
    for i in range(3):
        time.sleep(1)
    return x + y


@celery_app.task
def new_task():
    pass

## 定时任务定义