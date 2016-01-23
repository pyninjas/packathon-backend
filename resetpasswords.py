__author__ = 'pyninjas <info@pyninjas.com>'
__description__ = 'Tool for resetting and mailing passwords'

import os
import random
import string
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError

chars = string.ascii_letters + string.digits  # + '!@#$%^&*()'
length = 10
random.seed = (os.urandom(1024))

SUBJECT = 'Packathon Oylama Sistemi - Kullanıcı Bilgileri'
MESSAGE = """Merhaba {name},\nPackathon Parola: {password}\nURL: {url}\nBaşarılar dileriz\n\nPackathon.org"""


def random_password():
    """
    Get random password
    :return: str
    """
    return ''.join(random.choice(chars) for i in range(length))


def resetter():
    """
    Reset passwords and email them
    :return: None
    """
    users = get_user_model().objects.filter(is_active=True).exclude(username='admin')
    for user in users:
        password = random_password()
        user.set_password(password)
        user.save()
        try:
            send_mail(SUBJECT, MESSAGE.format(
                name=user.name,
                password=password,
                url='https://packathon.pyninjas.com'
            ), 'info@pyninjas.com', [user.email])
        except BadHeaderError as e:
            print("Error:")
            print(e)
            break
