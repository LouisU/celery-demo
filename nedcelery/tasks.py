from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.schedules import crontab
import time
import random
from requests import post
from celery.signals import task_success

TASK_RESULT = None


def pass_result(result):
    global TASK_RESULT
    TASK_RESULT = result


@shared_task
def my_task(task_type, code=None, command=None):

    if task_type == 'code':
        code = """{}
try:     
    result = func()
    pass_result(result)
except:
    raise Exception
""".format(code)
        # print(code)
        exec(code)
        return {"result": TASK_RESULT}

    elif task_type == 'python_script':

        try:
            import os
            result = os.system(command)
            # print("result:{}".format(result))
            return result
            # 'python /Users/louis/PycharmProjects/celery-demo/nedcelery/task/task_redis.py'
        except:
            raise Exception


# @task_success.connect(sender='my_task')
# def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
#     # information about task are located in headers for task messages
#     # using the task protocol version 2.
#     info = headers if 'task' in headers else body
#     print('after_task_publish for task id {info[id]}'.format(
#         info=info,
#     ))


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

# # 异步任务定义
# @shared_task
# def add(x, y):
#     for i in range(3):
#         pass
#         # time.sleep(1)
#     return x + y
#
#
# @shared_task(bind=True)
# def add_result(self, x, y):
#
#     # time.sleep(5)
#
#     return {'x': x, 'y': y, 'x+y': x+y}
#
#
# @shared_task
# def sub_result(x, y):
#     # time.sleep(5)
#     return {'x': x, 'y': y, 'x-y': x-y}
#
#
# @shared_task
# def long_task(n):
#     print('This task will take {} seconds.'.format(n))
#     for i in range(n):
#         print(i)
#         # time.sleep(1)
#
#
# @shared_task
# def multi_result(x, y):
#     # time.sleep(5)
#     return {'x': x, 'y': y, 'x-y': x * y}
#
#
