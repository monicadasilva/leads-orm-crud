from app.exceptions.exceptions import InvalidInput, InvalidKey, InvalidPhonePattern
import re
from datetime import datetime
import html
import pytz


def verify(data):

    exepected_keys = ['name', 'email', 'phone']
    data_keys = data.keys()
    wrong_keys = list(filter(lambda x: x not in data_keys, exepected_keys))
    invalid_values = []

    for values in data.values():
        if type(values) != str:
            invalid_values.append(values)

    if invalid_values:
        raise InvalidInput({'error': 'All fields must be a string.'})

    if wrong_keys:
        raise InvalidKey({'error': 'Only name, email and phone keys are allowed'})

    return ''


def check_phone_pattern(data):

    phone = data['phone']
    phone_pattern = r"\(?\d{2,}\)?[-]?\d{5,}[\-\s]?\d{4}"

    match = re.fullmatch(phone_pattern, phone)

    if match is None:
        raise InvalidPhonePattern({'error': 'Wrong phone pattern, the accepted pattern is (xx)xxxxx-xxxx.'})

    return ''


def sanitize(data):
    output = []
    recived_keys = []
    exepected_keys = ['name', 'email', 'phone']

    for keys, value in data.items():
        if keys in exepected_keys:
            recived_keys.append(keys)
            output.append(html.escape(value))

    input_sanatize = dict(zip(recived_keys, output))

    today = datetime.now(pytz.timezone('GMT'))

    creation_date = today.strftime("%a, %d %b %Y %H:%M:%S %Z")

    dates = {"creation_date": creation_date, "last_visit": creation_date}

    input_sanatize.update(dates)

    return input_sanatize
