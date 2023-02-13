import re

def valid_schedule(schedule):
    try:
        dateObject = datetime.datetime.strptime(date_string, date_format)
    except ValueError:
        return False
    return True

def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    return False

def valid_phone_number(phone_number):
    regex = r'^\+?(44)?(0|7)\d{9,13}$'
    if re.fullmatch(regex, phone_number):
        return True
    return False
