from celery import Celery
from datetime import timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

simple_app = Celery('workers', broker='RabbitMQ')
simple_app.conf.timezone = 'Asia/Kolkata'
simple_app.conf.beat_schedule = {
    'run_script_every_second': {
        'task': 'tasks.script_one',
        'schedule': timedelta(seconds=1),
    }
}

@app.route('/run', methods=['POST'])
def run_script():
    content = request.json
    additional_args = content["args"]
    script_id = content["script_id"]
    task = simple_app.send_task(f'tasks_queue.script_{script_id}', kwargs={'args': additional_args})
    # set script status to 'RUNNING' in firestore for this user
    app.logger.info(f'Script with script id: {script_id} & task id: {task.id} STARTED.')
    return jsonify({"task_id": task.id}), 202

@app.route('/stop', methods=['POST'])
def stop_script():
    content = request.json
    task_id = content["task_id"]
    simple_app.control.revoke(task_id, terminate=True)
    # set script status to 'STOPPED' in firestore for this user
    app.logger.info(f'Script with task id: {task_id} STOPPED.')
    return jsonify({"result": "script stopped"}), 202

@app.route('/get_status/<task_id>', methods=['GET'])
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    return status

if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)