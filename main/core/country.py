import json

from flask import Flask, jsonify
from loguru import logger

from src.microservice.three_microservices.libraries import Libs

SERVICE_NAME = 'COUNTRY'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/<name>', methods=['GET'])
def get_country_info(name: str):
    logger.info("Received input | country= " + name)
    data = _get_data()
    country_data = data.get(name)
    if country_data is None:
        return jsonify({'error': 'Country not found'}), 404
    else:
        logger.info("Country data:\n%s", json.dumps(country_data, indent=2))

    return jsonify(country_data)


def _get_data():
    return {
        'Poland': {
            'capital': 'Warsaw',
            'currency': 'PLN'
        },
        'USA': {
            'capital': 'Washington, D.C.',
            'currency': 'USD'
        },
        'Canada': {
            'capital': 'Ottawa',
            'currency': 'CAD'
        }
    }


if __name__ == '__main__':
    _port = int(Libs().read_configuration().get('country').split(":")[-1])
    app.run(port=_port)
