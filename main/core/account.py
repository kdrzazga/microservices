import threading
from collections import deque
from datetime import datetime

import yaml
from flask import Flask, Response, jsonify, request
from flask_httpauth import HTTPBasicAuth
from loguru import logger

SERVICE_NAME = 'ACCOUNT'

app = Flask(__name__)

users = {
    "admin": "admin"
}

basic_auth = HTTPBasicAuth()
info_cache = deque(maxlen=7)
stats = {
    'time-since-last-request': '-1',
    'total-request-count': '1',
    'total-request-browser-count': '1',
    'requests-in-recent-30': '1'
}


def reset_stats():
    global stats
    stats = {
        'time-since-last-request': '-1',
        'total-request-count': '1',
        'total-request-browser-count': '1',
        'requests-in-recent-30': '1'
    }
    logger.info("Statistics cleared")
    threading.Timer(9, reset_stats).start()


@basic_auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == users['admin']


@app.route('/', methods=['GET'])
def say_hello() -> str:
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/<account_id>', methods=['GET'])
@basic_auth.login_required
def get_account_info(account_id: int) -> Response:
    logger.info(SERVICE_NAME + " Getting info about " + str(account_id))
    client_info = _check_client()
    if float(client_info['time-since-last-request']) < 1.7:
        return jsonify({'error': 'Too many requests. Wait a few seconds'}), 429, {'Content-Type': 'application/json'}
    elif int(client_info['requests-in-recent-30']) > 8:
        return jsonify({'error': 'Too early. The requests will not be processed at the moment'}), 425, {
            'Content-Type': 'application/json'}

    with open('accounts.yml', 'r') as file:
        content = yaml.safe_load(file)
        for record in content['accounts']:
            logger.info('Record: ' + "|".join([f'{key} : {value}' for key, value in record.items()]))
            if str(record['id']) == account_id:
                return jsonify(record), 200, {'Content-Type': 'application/json'}

    return jsonify({'error': 'Account not found'}), 204, {'Content-Type': 'application/json'}  # 204 - no content


def _check_client():
    period = 15
    info = {'ip': request.remote_addr, 'browser': request.headers.get('User-Agent'),
            'date': datetime.now().strftime('%d %b %Y %H:%M:%S')}

    # Calculate elapsed time since the last request in the cache
    if len(info_cache) > 0:
        last_request_time = datetime.strptime(info_cache[-1]['date'], '%d %b %Y %H:%M:%S')
        elapsed_time = datetime.now() - last_request_time
        logger.info(f'Time since last request: {elapsed_time.total_seconds()} seconds')
        stats['time-since-last-request'] = str(elapsed_time.total_seconds())

        # Count the number of requests from the same IP address as in info
        ip_count = sum(1 for i in info_cache if i['ip'] == info['ip'])
        logger.info(f'Requests from IP {info["ip"]}: {ip_count}')
        stats['total-request-count'] = str(ip_count)

        # Count the number of requests from the same IP and browser as in info
        ip_browser_count = sum(1 for i in info_cache if i['ip'] == info['ip'] and i['browser'] == info['browser'])
        logger.info(f'Requests from IP {info["ip"]} and browser {info["browser"]}: {ip_browser_count}')
        stats['total-request-browser-count'] = str(ip_count)

        # Count the number of requests in the last 30 seconds
        recent_requests = [i for i in info_cache if (
                datetime.now() - datetime.strptime(i['date'], '%d %b %Y %H:%M:%S')).total_seconds() <= period]
        logger.info(f'Recent requests: {len(recent_requests)}')
        stats['requests-in-recent-30'] = str(ip_count)

    # Append the new request to the cache
    info_cache.append(info)

    return stats


if __name__ == '__main__':
    reset_stats()
    app.run(port=5957)
