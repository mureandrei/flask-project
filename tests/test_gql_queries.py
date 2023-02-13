import unittest
import tests.constants as constants
from flask import Flask
from gql_queries import resolve_create_customer
from db import db


class TestGQLQueries(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # drop everything for future tests
        with self.app.app_context():
            db.drop_all()

    def test_resolve_create_customer(self):
        value = {
            'customer': {
                'id': 1,
                'address': constants.ADDRESS,
                'email_address': constants.VALID_EMAIL,
                'first_name': constants.FIRST_NAME,
                'last_name': constants.LAST_NAME,
                'phone_number': constants.VALID_PHONE_NUMBER
            }
        }
        with self.app.app_context():
            assert value == resolve_create_customer(None,
                                                    None,
                                                    constants.FIRST_NAME,
                                                    constants.LAST_NAME,
                                                    constants.ADDRESS,
                                                    constants.VALID_PHONE_NUMBER,
                                                    constants.VALID_EMAIL)

    def test_resolve_create_customer_invalid_email(self):
        value = {'errors': ['Invalid email address format']}
        with self.app.app_context():
            assert value == resolve_create_customer(None,
                                                    None,
                                                    constants.FIRST_NAME,
                                                    constants.LAST_NAME,
                                                    constants.ADDRESS,
                                                    constants.VALID_PHONE_NUMBER,
                                                    constants.INVALID_EMAIL)
