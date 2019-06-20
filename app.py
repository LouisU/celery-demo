from flask import Flask
from redis import Redis

app = Flask(__name__)
rs = Redis(host='redis', port=6379, db=0)


@app.route('/name')
def add_name():
    rs.hset('name', 'louis', 'a')
    return "set name louis a"


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
