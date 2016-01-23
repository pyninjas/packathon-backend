from rest_framework import viewsets
from django.http import JsonResponse, Http404
from django.contrib.auth import get_user_model
from common.serializers import HackerSerializer
from common.models import Settings


class HackerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = HackerSerializer
    filter_fields = ('first_name', 'team')


def votetime(request):
    """
    Get beginning time for voting
    :param request: Django Request
    :return: json
    """
    time = Settings.objects.all()
    if len(time) < 1:
        raise Http404('Please set settings before using app')
    return JsonResponse({
        'start': time[0].vote_start_time,
        'end': time[0].vote_end_time})
