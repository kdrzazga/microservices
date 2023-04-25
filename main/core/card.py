import yaml
from loguru import logger
from flask import Flask, jsonify, json, Response
from flask_httpauth import HTTPBasicAuth

SERVICE_NAME = 'CARD'

app = Flask(__name__)

users = {
    "admin": "admin"
}

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == users['admin']


@app.route('/', methods=['GET'])
def say_hello() -> str:
    logger.info("Hello from service " + SERVICE_NAME)
    return 'Microservice %s' % SERVICE_NAME


@app.route('/<card_type>/<card_id>', methods=['GET'])
@basic_auth.login_required
def read_card(card_type: str, card_id: int) -> Response:
    logger.info("Request for " + card_type + " [" + str(card_id) + "]")

    with open('cards.yml', 'r') as file:
        cards = yaml.safe_load(file)

    selected_cards = cards['credit-card'] if card_type == 'credit' else cards['debit-card']
    logger.info("Card data:\n%s", json.dumps(selected_cards, indent=2))

    return jsonify(_get_card_by_id(selected_cards, card_id))


def _get_card_by_id(cards, card_id: int):
    for card in cards:
        if str(card['id']) == card_id:
            return card
    return None


if __name__ == '__main__':
    app.run(port=5955)
