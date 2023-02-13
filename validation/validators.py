import datetime
import re

from flask_sqlalchemy import SQLAlchemy
from models.customer import Customer

INVALID_EMAIL_ERROR = "Invalid email address format"
INVALID_SCHEDULE_ERROR = "Invalid schedule time format"
INVALID_PHONE_NUMBER_ERROR = "Invalid phone number format"
INVALID_CUSTOMER_ID_ERROR = "Invalid customer ID"

class Validator:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def validate_customer(self, **args):
        errors = [
            self._validate_phone_number(args['phone_number']),
            self._validate_email(args['email_address'])
        ]
        return self._filter_errors(errors)

    def validate_work_order(self, **args):
        errors = [
            self._validate_customer_id(args['customer_id']),
            self._validate_schedule(args['schedule'])
        ]
        return self._filter_errors(errors)

    def _filter_errors(self, errors):
        filtered_errors = filter(lambda error: error != None, errors)
        filtered_errors = [error for error in filtered_errors]
        if len(filtered_errors):
            return filtered_errors
        return None
    
    def _validate_schedule(self, schedule) -> str | None:
        try:
            datetime.datetime.strptime(schedule, "%d-%m-%Y")
        except ValueError:
            return INVALID_SCHEDULE_ERROR
        return None

    def _validate_email(self, email) -> str | None:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, email):
            return None
        return INVALID_EMAIL_ERROR

    def _validate_phone_number(self, phone_number) -> str | None:
        regex = r'^\+?(44)?(0|7)\d{9,13}$'
        if re.fullmatch(regex, phone_number):
            return None
        return INVALID_PHONE_NUMBER_ERROR
    
    def _validate_customer_id(self, customer_id) -> str | None:
        customer = self.db.session.get(Customer, customer_id)
        if customer:
            return None
        return INVALID_CUSTOMER_ID_ERROR
