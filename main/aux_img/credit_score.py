import json, requests

import loguru
from flask import Flask, jsonify
from datetime import timedelta
from loguru import logger

SERVICE_NAME = 'CREDIT SCORE'
app = Flask(__name__)
loguru.logger.add("credit_score.log", rotation="10 minutes", retention=timedelta(minutes=10))


@app.route('/', methods=['GET'])
def say_hello():
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


# TODO
""" 
@app.route('/<account_id>', methods=['GET'])
def get_credit_info(account_id: int):
    logger.info("Received request: Credit Score for account: " + account_id)
    account = requests.get()
    data = _get_data()
    country_data = data.get(name)
    if country_data is None:
        return jsonify({'error': 'Country not found'}), 404
    else:
        logger.info("Country data:\n%s", json.dumps(country_data, indent=2))

    return jsonify(country_data)
"""

if __name__ == '__main__':
    app.run(port=6011)
