__author__ = 'pyninjas <info@pyninjas.com>'
__description__ = 'Tool for importing data from csv file'

import csv
from django.contrib.auth import get_user_model
from team.models import Team


def importer():
    """
    Import users from csv file
    :return: None
    """
    csvfile = open('takimlar.csv', 'r')
    teams = csv.reader(csvfile)
    counter = 1
    for data in teams:
        team = Team.objects.create(name=data[0])
        team.save()
        username = data[4].split('@')[0]
        if username == 'admin':
            username += str(counter)
            counter += 1
        if len(username) < 3:
            username += str(counter)
            counter += 1
        password = data[4].split('@')[0][0] + data[4].split('@')[0][-1] + '123456'
        print("Username: %s\nPassword: %s" % (username, password))
        user = get_user_model().objects.create_user(
            username=username,
            email=data[4],
            password=password,
            name=data[2] + ' ' + data[3],
            team=team)
        user.save()
