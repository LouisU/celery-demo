#
from celery import shared_task, task
from celery.schedules import crontab
import time
import random
from requests import post


# 异步任务定义
@shared_task
def add(x, y):
    for i in range(3):
        time.sleep(1)
    return x + y


@shared_task(bind=True)
def add_result(self, x, y):

    time.sleep(30)

    return {'x': x, 'y': y, 'x+y': x+y}


@shared_task
def long_task(n):
    print('This task will take {} seconds.'.format(n))
    for i in range(n):
        print(i)
        time.sleep(1)



# @task(bind=True)
# def long_task(self, elementid, userid, url):
#     """Background task that runs a long function with progress reports."""
#     verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
#     adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
#     noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
#     message = ''
#     total = random.randint(10, 50)
#     for i in range(total):
#         if not message or random.random() < 0.25:
#             message = '{0} {1} {2}...'.format(random.choice(verb),
#                                               random.choice(adjective),
#                                               random.choice(noun))
#         meta = {'current': i, 'total': total, 'status': message,
#                 'elementid': elementid, 'userid': userid}
#         post(url, json=meta)
#         time.sleep(0.5)
#
#     meta = {'current': 100, 'total': 100, 'status': 'Task completed!',
#             'result': 42, 'elementid': elementid, 'userid': userid}
#     post(url, json=meta)
#     return meta