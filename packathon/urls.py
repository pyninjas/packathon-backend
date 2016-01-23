"""
Django urls
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from common.views import HackerViewSet, votetime
from team.views import TeamViewSet
from project.views import ProjectViewSet
from feed.views import FeedViewSet
from web import views

admin.autodiscover()

router = routers.DefaultRouter()
# Users
router.register(r'users', HackerViewSet)
# Teams
router.register(r'teams', TeamViewSet)
# Projects
router.register(r'projects', ProjectViewSet)
# Feeds
router.register(r'feeds', FeedViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include('rest_auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/votetime', votetime),
    url(r'^projects/add', views.add_project),
    url(r'^projects/(?P<pk>\d+)', views.projects, name='project-view'),
    url(r'^projects/', views.projects),
    url(r'^teams/(?P<pk>\d+)', views.teams),
    url(r'^teams/', views.teams),
    url(r'^feed/', views.feed),
    url(r'^users/(?P<pk>\d+)/', views.profile, name='user-profile'),
    url(r'^login/', views.login_view),
    url(r'^$', views.index, name='index'),
]
