import json

import yaml
from flask import Flask, jsonify
from loguru import logger

SERVICE_NAME = 'COUNTRY'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def say_hello():
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/which_country/<city_name>', methods=['GET'])
def find_country(city_name: str):
    all_countries = _get_data()
    for country in all_countries:
        if city_name in all_countries[country]['cities']:
            return jsonify(country), 200,\
                   {'Content-Type': 'application/json'}  # 200 - OK

    return jsonify("City not found. It can still exists though,"
                   " just not in our database."), 204, {
        'Content-Type': 'application/json'}  # 204 - no content


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
        "Poland": {
            "capital": "Warsaw",
            "currency": "PLN",
            "cities": ["Namyslow", "Gdansk", "Wroclaw"]
        },
        "USA": {
            "capital": "Washington, D.C.",
            "currency": "USD",
            "cities": ["New York", "Los Angeles", "Chicago"]
        },
        "Canada": {
            "capital": "Ottawa",
            "currency": "CAD",
            "cities": ["Toronto", "Vancouver", "Montreal"]
        }
    }


if __name__ == '__main__':
    config_file = r"configuration.yml"  # provide the file path here

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    _port = config["hosts"]["country"].split(":")[-1]

    print("http://127.0.0.1:" + str(_port) + "/USA")
    print("http://127.0.0.1:" + str(_port) + "/Poland")
    print("http://127.0.0.1:" + str(_port) + "/Canada")
    print("http://127.0.0.1:" + str(_port) + "/which_country/Chicago")
    print("http://127.0.0.1:" + str(_port) + "/which_country/Namyslow")
    print("http://127.0.0.1:" + str(_port) + "/which_country/Gdansk")
    print("http://127.0.0.1:" + str(_port) + "/which_country/Toronto")
    print("http://127.0.0.1:" + str(_port) + "/which_country/Montreal")
    app.run(port=_port)
