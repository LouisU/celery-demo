
from celery import Celery

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_URL = 'amqp://user:password@rabbitmq:5672/my_vhost'

CELERY_RESULT_BACKEND = 'redis://redis:6379/2'

celery_app = Celery('celery-app',
                    broker=CELERY_BROKER_URL,
                    backend=CELERY_RESULT_BACKEND)
# celery_app.config_from_object('.:config', namespace='CELERY')

celery_app.autodiscover_tasks()

CELERYD_MAX_TASKS_PER_CHILD = 10

# celery -A celery-demo beat -l INFO
# celery -A celery-demo worker -l INFO
# celery -A celery-demo worker -b -l info

#

if __name__ == "__main__":

    # print(celery_app.broker_connection)
    pass