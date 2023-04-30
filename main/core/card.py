from datetime import datetime

import yaml
from flask import Flask, jsonify, json, Response, render_template
from flask_httpauth import HTTPBasicAuth
from loguru import logger

SERVICE_NAME = 'CARD'

app = Flask(__name__)

users = {
    "admin": "admin"
}

recently_deleted = []
protected = {1234}

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == users['admin']


@app.route('/', methods=['GET'])
def serve_page():
    logger.info("Hello from service " + SERVICE_NAME)
    return render_template('card_request.html')


@app.route('/read/<card_id>', methods=['GET'])
def read_card_old(*args, **kwargs) -> Response:
    message = "Info about cards available at /<card_type>/<card_id>"
    logger.warning(message)
    return jsonify(message), 308, {'Content-Type': 'application/json'}  # 308 permanent redirect


@app.route('/read/<card_type>/<card_id>', methods=['GET'])
@basic_auth.login_required
def read_card(card_type: str, card_id: int) -> Response:
    logger.info("Request for " + card_type + " [" + str(card_id) + "]")

    if card_id in recently_deleted:
        return jsonify("No more information about this card. Must have been deleted recently."), 204, \
               {'Content-Type': 'application/json'}  # 204 No Content

    with open('cards.yml', 'r') as file:
        cards = yaml.safe_load(file)

    selected_cards = cards['credit-card'] if card_type == 'credit' else cards['debit-card']
    logger.info("Card data:\n%s", json.dumps(selected_cards, indent=2))

    return jsonify(_get_card_by_id(selected_cards, card_id)), 200, {'Content-Type': 'application/json'}  # 200 OK


@app.route('/create/<name>/<customer_name>/<account_ref>', methods=['POST'])
@basic_auth.login_required
def create_credit_card(name, customer_name, account_ref, issue_date=None, file_path='cards.yml') -> Response:
    new_id = create_credit_card_service(name, account_ref, customer_name, file_path, issue_date)
    return jsonify('Card created id=' + str(new_id)), 201, {'Content-Type': 'application/json'}  # 201 Created


@app.route('/delete/<card_type>/<card_id>', methods=['DELETE'])
@basic_auth.login_required
def delete_card(card_id, card_type) -> Response:
    if card_id in protected:
        message = "No authorization to delete card[id = " + str(card_id) + "]. No one can delete it."
        logger.info(message)
        return jsonify(message), 405, {'Content-Type': 'application/json'}  # 405 Method Not Allowed

    success = delete_credit_card_service(card_id, card_type)

    if success:
        recently_deleted.append(card_id)

    return jsonify('Card deleted id=' + str(card_id)), 410, {'Content-Type': 'application/json'}  # 410 Gone


def create_credit_card_service(name, account_ref, customer_name, file_path='cards.yml', issue_date=None):
    # Load the YAML file
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # Find the highest existing ID in the credit card list
    existing_ids = [card['id'] for card in data['credit-card']]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    # Set a default issue date of the current date and time
    if issue_date is None:
        issue_date = datetime.now().strftime('%Y-%m-%d')

    # Create a new credit card dictionary with the assigned ID and default issue date
    new_card = {'id': new_id,
                'name': name,
                'customer-name': customer_name,
                'issue-date': issue_date,
                'account-ref': account_ref}

    # Add the new card to the credit card list
    data['credit-card'].append(new_card)

    # Save the updated YAML file
    with open(file_path, 'w') as file:
        yaml.dump(data, file)
    return new_id


def delete_credit_card_service(card_id, card_type='credit-card', file_path='cards.yml'):
    # Load the YAML file
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    for record in data[card_type]:
        if record['id'] == card_id:
            data[card_type].remove(record)
            break  # stop searching after the first match

    # Save the updated YAML file
    with open(file_path, 'w') as file:
        yaml.dump(data, file)
    return True


def _get_card_by_id(cards, card_id: int):
    for card in cards:
        if str(card['id']) == card_id:
            return card
    return None


if __name__ == '__main__':
    app.run(port=5955)
