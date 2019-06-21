from flask import Flask, jsonify, Response, url_for, session
import uuid
from redis import Redis
from nedcelery import tasks
import time
from celery import Celery
from flask_socketio import SocketIO, join_room
from random import randint
import json



app = Flask(__name__)
app.secret_key="DataRoadReflect"

# app.config['CELERY_BROKER_URL'] = 'amqp://user:password@rabbitmq:5672/my_vhost'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/2'
#
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

socketio = SocketIO(app, message_queue="amqp://guest:guest@localhost:5672/socketio")
rs = Redis(host='localhost', port=6379, db=0)


@socketio.on('connect')
def socket_connect():
    pass


@app.route('/taskn')
def add_name():
    rs.hset('name', 'louis', 'a')
    tasks.add.delay(2, 9)
    return jsonify({'progress': True})


@app.route('/taskadd')
def x_add_y():
    # 任务对象 Agent证书=Queue名字
    task = tasks.add_result.apply_async(args=[10, 20], queue='louis-demo2')
    return jsonify({'progressing': 'true', 'task_id': task.id}), 202, {'Location': url_for(
        'taskstatus', task_id=task.id
    )}
    # return jsonify({'result': 'true'})


@app.route('/status/<task_id>')
def taskstatus(task_id):

    print(task_id)
    task = tasks.add_result.AsyncResult(task_id)
    print(task.state)

    return jsonify({'status': task.state, 'task_id': task_id})


@app.route('/task/<task_id>')
def task_check(task_id):

    redis_task_id = 'celery-task-meta-{}'.format(task_id)
    value = rs.get(redis_task_id)
    print(value)
    print(type(value))
    if value is not None:
        value = json.loads(value)
    else:
        value = 'in progressing'
    return jsonify({'result': value})


@app.route('/')
def hello_world():
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())

    return jsonify({'session_uid': session['uid']})


@socketio.on('join_room', namespace='/long_task')
def on_room():
    room = str(session['uid'])
    print('join room {}'.format(room))
    join_room(room)


@app.route('/runtask')
def long_task():

    n = randint(0, 100)
    print(session['uid'])
    sid = str(session['uid'])
    print(sid)
    task = tasks.long_task.delay(n=n)

    return jsonify({'id':task.id})


if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True, host="0.0.0.0")