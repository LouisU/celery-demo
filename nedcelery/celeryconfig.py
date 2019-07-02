from __future__ import absolute_import, unicode_literals

# celery configuration


# CELERY_ACCEPT_CONTENT = ['json']

accept_content = ['json']

# CELERY_TASK_SERIALIZER = 'json'

task_serializer = 'json'

# CELERY_BROKER_URL = 'amqp://user:password@rabbitmq:5672/my_vhost'
broker_url = 'amqp://guest:guest@127.0.0.1:5672/'

# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
result_backend = 'redis://127.0.0.1:6379/1'

imports = ('nedcelery.tasks',)


# app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@127.0.0.1:5672/'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

