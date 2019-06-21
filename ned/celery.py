
from celery import Celery
from app import app

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_URL = 'amqp://user:password@rabbitmq:5672/my_vhost'

CELERY_RESULT_BACKEND = 'redis://redis:6379/2'

app.config['CELERY_BROKER_URL'] = 'amqp://user:password@rabbitmq:5672/my_vhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/2'


instance = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
instance.conf.update(app.config)


# tell celery where to find the tasks
instance.autodiscover_tasks(['ned',])



# CELERYD_MAX_TASKS_PER_CHILD = 10

# celery -A ned.celery beat -l INFO
# celery -A ned.celery worker -l INFO
# celery -A ned.celery worker -b -l info


