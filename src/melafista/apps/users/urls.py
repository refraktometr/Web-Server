from django.conf.urls import patterns, include, url
from apps.users import views

urlpatterns = patterns('apps.users.views',
    url(r'^$', views.index),
    url(r'^registration/$', views.registration),
    url(r'^confirmation/user_id/(\d+)/$', views.confirmation),
    url(r'^logout/$', views.logout)
    )
