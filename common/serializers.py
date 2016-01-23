from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_gravatar.helpers import get_gravatar_url


class HackerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for user
    """
    photo = serializers.SerializerMethodField('get_gravatar_url')

    @staticmethod
    def get_gravatar_url(user):
        if user.email:
            return get_gravatar_url(user.email, size=256)
        # return default gravatar image if email is not set
        return 'http://www.gravatar.com/avatar/?d=identicon&r=g&s=256'

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'description', 'team',
                  'website', 'git', 'twitter', 'email', 'photo', 'password', 'url',
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, user, data=None):
        user.set_password(data['password'])
        user.save()
        return user


class CurrentHackerSerializer(HackerSerializer):
    """
    Serializer for current user
    """
    voted_project = serializers.SerializerMethodField('get_project')

    @staticmethod
    def get_project(user):
        if not user.voted_for:
            return None
        return user.voted_for.pk

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'description', 'team', 'website',
                  'git', 'twitter', 'email', 'photo', 'password', 'url', 'voted_project'
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }
