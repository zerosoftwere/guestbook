from flask import Flask, render_template, request, redirect
from redis import Redis
from time import time
import json
import os

REDIS_MASTER_HOST = 'redis-master'
REDIS_SLAVE_HOST = 'redis-slave'
REDIS_PORT = 6379

if os.environ.get('GET_HOSTS_FROM') == 'env':
    REDIS_MASTER_HOST = os.environ.get('REDIS_MASTER_SERVICE_HOST')
    REDIS_SLAVE_HOST = os.environ.get('REDIS_SLAVE_SERVICE_HOST')

redis_master = Redis(host=REDIS_MASTER_HOST, port=REDIS_PORT)
redis_slave = Redis(host=REDIS_SLAVE_HOST, port=REDIS_PORT)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    entries = redis_slave.lrange('entries', 0, -1) or []
    if request.method == 'GET':
        return render_template('index.html', entries=entries)
    elif request.method == 'POST':
        content = request.form.get('content')
        if content.strip():
            redis_master.lpush('entries', content)
        return redirect('/')

@app.route('/clear')
def clear():
    redis_master.delete('entries')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
