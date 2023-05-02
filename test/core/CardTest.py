import yaml
import unittest
from datetime import datetime
from loguru import logger

from main.core.card import create_credit_card_service, del_credit_card_srv


class CardTest(unittest.TestCase):
    def test_create_credit_card(self):
        now = datetime.now().strftime('%Y-%m-%d')
        file_path = '../../main/core/cards.yml'
        new_id = create_credit_card_service('Visa', 'Ian Tester', 3456, file_path, now)

        with open(file_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        # Find the highest existing ID in the credit card list
        card_type = 'credit-card'
        existing_ids = [card['id'] for card in data[card_type]]

        self.assertIn(new_id, existing_ids)
        logger.info("Created " + card_type + " with id = " + str(new_id))
        logger.info("Deleting " + str(new_id) + "...")
        # clean up
        del_credit_card_srv(new_id, card_type, file_path)


if __name__ == '__main__':
    unittest.main()
