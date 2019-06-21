
# celery configuration

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_URL = 'amqp://user:password@rabbitmq:5672/my_vhost'

CELERY_RESULT_BACKEND = 'redis://redis:6379/2'