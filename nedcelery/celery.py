
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import time
# from importlib import import_module, reload


celery = Celery('celery_app')
celery.config_from_object('nedcelery.celeryconfig')


# def import_string(import_name):
#     import_name = str(import_name).replace(':', '.')
#     modules = import_name.split('.')
#     mod = import_module(modules[0])
#     for comp in modules[1:]:
#         if not hasattr(mod, comp):
#             reload(mod)
#         mod = getattr(mod, comp, None)
#     return mod
#
#
# @celery.task
# def execute(func, *args, **kwargs):
#     func = import_string(func)
#     return func(*args, **kwargs)

# app.py中调用
# @app.route('/execute')
# def test_execute():
#     task = execute.apply_async('task.all_task.ee', 2, 444)
#     return jsonify({'task_id': task.id})



# celery -A nedcelery.celery beat -l INFO
# celery -A nedcelery.celery worker -l INFO
# celery -A nedcelery.celery worker -b -l info
if __name__ == "__main__":
    print("Hello World!")