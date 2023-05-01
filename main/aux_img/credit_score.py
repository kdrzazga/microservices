import json
import loguru
import requests
import yaml

from datetime import timedelta
from flask import Flask, jsonify
from loguru import logger

SERVICE_NAME = 'CREDIT SCORE'
app = Flask(__name__)
loguru.logger.add("credit_score.log", rotation="10 minutes", retention=timedelta(minutes=10))

data = {}
accounts_host = ""


@app.route('/', methods=['GET'])
def say_hello():
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/<account_id>', methods=['GET'])
def get_credit_info(account_id: int):
    logger.info("Received request: Credit Score for account: " + str(account_id))
    _check_account_service()
    url = accounts_host + "/" + str(account_id)

    logger.info("Reading accounts from " + url)
    response = requests.get(url, auth=('admin', 'admin'))

    if response.status_code == 200:
        account = response.json()
    if account is None:
        return jsonify({'error': 'Account not available.'}), 404, {
            'Content-Type': 'application/json'}  # 404 - not found

    logger.info("Read info about account:\n" + json.dumps(account, indent=2))
    logger.info("Account balance: " + str(account['balance']))

    result = int(account['balance']) > 3000
    return jsonify(result), 200, {'Content-Type': 'application/json'}  # 200 - OK


def _check_account_service():
    logger.info("Accounts host: " + accounts_host)
    response = requests.get(accounts_host, auth=('admin', 'admin'))

    availability = " " if response.status_code == 200 else " not "
    logger.info("Service ACCOUNT is" + availability + "available")


def init():
    global data, accounts_host
    with open('configuration.yml', 'r') as stream:
        data = yaml.safe_load(stream)
    if data is not None:
        logger.info("Read configuration")
        logger.info("")
        accounts_host = data['hosts']['account']
        logger.info("Accounts host: " + accounts_host)


if __name__ == '__main__':
    init()
    app.run(port=6011)
