from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    worker_id = os.environ.get('WORKER_ID', 'unknown')
    return jsonify({
        'message': f'Hello from worker {worker_id}',
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
