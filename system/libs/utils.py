import json
import random
import re
import time
import uuid
import unidecode
from datetime import datetime
from subprocess import Popen, PIPE

from django.conf import settings
from django.contrib.auth.hashers import get_hasher
from django.template.defaultfilters import slugify
from django.utils import timezone


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(date_time):
    return int(time.mktime(date_time.timetuple()))


def get_timestamp():
    return int(timezone.now().timestamp())


def get_now():
    return timezone.now()


def get_equivalent_char(char):
    char = str(char).lower()
    if char == '@' or char == '4' or char == 'á':
        return 'a'
    elif char == '3' or char == '€' or char == 'é':
        return 'e'
    elif char == '1' or char == '&' or char == 'í':
        return 'i'
    elif char == '0' or char == 'ó':
        return 'o'
    elif char == 'ú':
        return 'u'
    elif char == '$':
        return 's'
    elif not char.isalpha() and not char.isnumeric():
        return ' '
    else:
        return char


def validate_text(text):
    text = str(text).lower()
    content = open(str(settings.BASE_DIR / 'system' / 'libs' / 'json' / 'denied_words.json')).read()
    words = json.loads(content)
    found = []
    new_text = ''
    for char in text:
        new_text += get_equivalent_char(char)
    new_text = re.sub(r'\s\s+', ' ', new_text)
    split = new_text.split(' ')
    for word in split:
        if word in words:
            found.append(word)
    return found


def unique_slug(name, mayor=100):
    hasher = get_hasher('default')
    return slugify(name)[:mayor] + '-' + str(hasher.salt())


def generate_key():
    hasher = get_hasher('default')
    return hasher.salt() + hasher.salt() + hasher.salt()


def generate_string(special_character=False, n=10):
    return ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*!@#$%^&()+=:;{}[]<>?/,.-_ ') for i
        in range(0, n)) if special_character else ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(0, n))


def generate_num(n=9):
    return ''.join(random.choice('0123456789') for i in range(0, n))


def get_client_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if request.META.get(
        'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')


def script(script_text):
    p = Popen(args=script_text, shell=True, stdout=PIPE, stdin=PIPE)
    output, errors = p.communicate()
    return output, errors


def get_uuid(name=None):
    return str(uuid.uuid3(uuid.NAMESPACE_OID, name)) if name else str(uuid.uuid4())


def remove_accents(data):
    return unidecode.unidecode(data)


def merge_two_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
