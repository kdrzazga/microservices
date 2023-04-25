import yaml
from flask import Flask, Response, jsonify
from flask_httpauth import HTTPBasicAuth
from loguru import logger

SERVICE_NAME = 'ACCOUNT'

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


@app.route('/<account_id>', methods=['GET'])
@basic_auth.login_required
def get_account_info(account_id: int) -> Response:
    logger.info(SERVICE_NAME + " Getting info about " + str(account_id))
    with open('accounts.yml', 'r') as file:
        content = yaml.safe_load(file)
        for record in content['accounts']:
            logger.info('Record: ' + "|".join([f'{key} : {value}' for key, value in record.items()]))
            if str(record['id']) == account_id:
                return jsonify(record)

    return jsonify({'error': 'Account not found'})


if __name__ == '__main__':
    app.run(port=5957)
