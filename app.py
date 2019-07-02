from flask import Flask, jsonify, Response, url_for, session, request
import uuid
from redis import Redis
from nedcelery import tasks
import time
from celery import Celery
from flask_socketio import SocketIO, join_room
from random import randint
import json


app = Flask(__name__)

# args about socket io
app.secret_key = "DataRoadReflect"
socketio = SocketIO(app, message_queue="amqp://guest:guest@localhost:5672/socketio")

# set redis
rs = Redis(host='localhost', port=6379, db=1)


@socketio.on('connect')
def socket_connect():
    pass


@app.route('/async_task', methods=['POST',])
def async_task():

    task_type = request.get_json().get('task_type', 'code')
    worker = request.get_json().get('worker', None)

    default_code = """
def func():
    import time
    sum = 0
    for i in range(30):
        time.sleep(1)
        sum += i
    return sum
"""

    file_path = 'task_redis.py'
    if task_type == "code":
        code = request.get_json().get('code', default_code)
        task = tasks.my_task.delay(task_type, code)
        return jsonify({'task_id': task.id})

    elif task_type == "python_script":
        from os import path
        directory = path.dirname(__file__)
        file_path = request.get_json().get('file_path', file_path)
        file_directory = directory + '/nedcelery/task/' + file_path
        command = 'python ' + file_directory
        print(command)
        task = tasks.my_task.delay('python_script', command)
        return jsonify({'task_id': task.id})


@app.route('/status/<task_id>')
def taskstatus(task_id):

    print(task_id)
    task = tasks.add_result.AsyncResult(task_id)
    print(task.state)

    return jsonify({'status': task.state, 'task_id': task_id})


@app.route('/task/<task_id>')
def task_check(task_id):

    redis_task_id = 'celery-task-meta-{}'.format(task_id)
    print(redis_task_id)
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






# @app.route('/taskn')
# def add_name():
#     rs.hset('name', 'louis', 'a')
#     tasks.add.delay(2, 9)
#     return jsonify({'progress': True})
#
#
# @app.route('/taskadd')
# def x_add_y():
#     # 任务对象 Agent证书=Queue名字
#     task = tasks.add_result.apply_async(args=[10, 20])
#     return jsonify({'progressing': 'true', 'task_id': task.id}), 202, {'Location': url_for(
#         'taskstatus', task_id=task.id
#     )}


# @app.route('/runtask')
# def long_task():
#
#     n = randint(0, 100)
#     print(session['uid'])
#     sid = str(session['uid'])
#     print(sid)
#     task = tasks.long_task.delay(n=n)
#
#     return jsonify({'id': task.id})
#
#
#
#
# @app.route('/tasksub')
# def sub_result():
#     task = tasks.sub_result.apply_async(args=[5,2])
#     return jsonify({'task_id': task.id})
#
#
# @app.route('/taskmulti')
# def sub_test():
#     task = tasks.multi_result.apply_async(args=[5,2])
#     return jsonify({'task_id': task.id})


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True, host="0.0.0.0")