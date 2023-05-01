import json
from datetime import timedelta

import loguru
import requests
import yaml
from flask import Flask, jsonify
from loguru import logger

SERVICE_NAME = 'CREDIT SCORE'
app = Flask(__name__)
loguru.logger.add("credit_score.log", rotation="10 minutes", retention=timedelta(minutes=10))


@app.route('/', methods=['GET'])
def say_hello():
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/<account_id>', methods=['GET'])
def get_credit_info(account_id: int):
    logger.info("Received request: Credit Score for account: " + str(account_id))
    with open('configuration.yml', 'r') as stream:
        data = yaml.safe_load(stream)

    host = data['hosts']['account']
    response = requests.get(host + "/" + str(account_id), auth=('admin', 'admin'))
    if response.status_code == 200:
        account = response.json()
    if account is None:
        return jsonify({'error': 'Account not available.'}), 404, {
            'Content-Type': 'application/json'}  # 404 - not found

    logger.info("Read info about account:\n" + json.dumps(account, indent=2))
    logger.info("Account balance: " + str(account['balance']))

    result = int(account['balance']) > 3000
    return jsonify(result), 200, {'Content-Type': 'application/json'}  # 200 - OK


if __name__ == '__main__':
    app.run(port=6011)
