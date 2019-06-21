from flask import Flask, jsonify, Response, url_for
from redis import Redis
from ned import tasks
import time
from celery import Celery


app = Flask(__name__)

# app.config['CELERY_BROKER_URL'] = 'amqp://user:password@rabbitmq:5672/my_vhost'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/2'
#
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)


rs = Redis(host='redis', port=6379, db=0)


@app.route('/taskn')
def add_name():
    rs.hset('name', 'louis', 'a')
    tasks.add.delay(2, 9)
    return jsonify({'progress': True})


@app.route('/taska')
def x_add_y():
    task = tasks.add_result.apply_async()
    return jsonify({'progressing'}), 202, {'Location': url_for(
        'taskstatus', task_id=task.id
    )}


@app.route('/status/<task_id>')
def task_status(task_id):

    task = tasks.add_result.AsyncResult(task_id)

    return jsonify({'status': task.state, 'task_id': task_id})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/louis')
def hello_louis():
    return 'Hello Louis!'


@app.route('/test')
def test():
    return 'this is a test'


if __name__ == '__main__':
    app.run(debug=True)
