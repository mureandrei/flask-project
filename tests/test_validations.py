from models.enums.work_order_type import WorkOrderType
from validation.validators import Validator
import tests.constants as constants

class MockSession:
    def __init__(self):
        self.session_get_return_value = None

    def set_session_get_return_value(self, session_get_return_value):
        self.session_get_return_value = session_get_return_value
    
    def get(self, model, _):
        return self.session_get_return_value

class MockDB:
    def __init__(self):
        self.session = MockSession()

validator = Validator(MockDB())


def test_invalid_customer_email_phone():
    customer_fields = {
        'first_name': constants.FIRST_NAME,
        'last_name': constants.LAST_NAME,
        'address': constants.ADDRESS,
        'phone_number': constants.INVALID_PHONE_NUMBER,
        'email_address': constants.INVALID_EMAIL
    }
    errors = validator.validate_customer(**customer_fields)
    assert len(errors) == 2
    assert errors[0] == 'Invalid phone number format'
    assert errors[1] == 'Invalid email address format'

def test_invalid_customer_email():
    customer_fields = {
        'first_name': constants.FIRST_NAME,
        'last_name': constants.LAST_NAME,
        'address': constants.ADDRESS,
        'phone_number': constants.VALID_PHONE_NUMBER,
        'email_address': constants.INVALID_EMAIL
    }
    errors = validator.validate_customer(**customer_fields)
    assert len(errors) == 1
    assert errors[0] == 'Invalid email address format'

def test_invalid_customer_phone():
    customer_fields = {
        'first_name': constants.FIRST_NAME,
        'last_name': constants.LAST_NAME,
        'address': constants.ADDRESS,
        'phone_number': constants.INVALID_PHONE_NUMBER,
        'email_address': constants.VALID_EMAIL
    }
    errors = validator.validate_customer(**customer_fields)
    assert len(errors) == 1
    assert errors[0] == 'Invalid phone number format'

def test_valid_customer():
    customer_fields = {
        'first_name': constants.FIRST_NAME,
        'last_name': constants.LAST_NAME,
        'address': constants.ADDRESS,
        'phone_number': constants.VALID_PHONE_NUMBER,
        'email_address': constants.VALID_EMAIL
    }
    errors = validator.validate_customer(**customer_fields)
    assert errors == None

def test_valid_work_order():
    work_order_fields = {
        "customer_id": 1,
        "schedule": constants.VALID_SCHEDULE,
        "work_order_type": WorkOrderType.INSTALL.value
    }
    validator.db.session.set_session_get_return_value({"customer": "customer"})
    errors = validator.validate_work_order(**work_order_fields)
    assert errors == None

def test_invalid_work_order_customer_id():
    work_order_fields = {
        "customer_id": 1,
        "schedule": constants.VALID_SCHEDULE,
        "work_order_type": WorkOrderType.INSTALL.value
    }
    validator.db.session.set_session_get_return_value(None)
    errors = validator.validate_work_order(**work_order_fields)
    assert len(errors) == 1
    assert errors[0] == "Invalid customer ID"

def test_invalid_work_order_schedule():
    work_order_fields = {
        "customer_id": 1,
        "schedule": constants.INVALID_SCHEDULE,
        "work_order_type": WorkOrderType.INSTALL.value
    }
    validator.db.session.set_session_get_return_value({"customer": "customer"})
    errors = validator.validate_work_order(**work_order_fields)
    assert len(errors) == 1
    assert errors[0] == "Invalid schedule time format"

def test_invalid_work_order_schedule_customer_id():
    work_order_fields = {
        "customer_id": 1,
        "schedule": constants.INVALID_SCHEDULE,
        "work_order_type": WorkOrderType.INSTALL.value
    }
    validator.db.session.set_session_get_return_value(None)
    errors = validator.validate_work_order(**work_order_fields)
    assert len(errors) == 2
    assert errors[0] == "Invalid customer ID"
    assert errors[1] == "Invalid schedule time format"
