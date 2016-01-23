from requests import post
from json import dumps
from django.conf import settings


class Push(object):
    """
    Custom class for push notifications using parse
    """
    def __init__(self):
        application = getattr(settings, "PARSE_APPLICATION_ID", None)
        api_key = getattr(settings, "PARSE_APPLICATION_KEY", None)
        self.url = 'https://api.parse.com/1/push'
        self.data = {
            'where': {},
            'data': {
                'alert': ''
            }
        }
        self.headers = {
            'X-Parse-Application-Id': application,
            'X-Parse-REST-API-Key': api_key,
            'Content-Type': 'application/json'
        }

    def send(self, message):
        """
        :return: Return message, Status code
        """
        self.data['data']['alert'] = message
        r = post(self.url, data=dumps(self.data), headers=self.headers)
        return r.text, r.status_code

pusher = Push()
