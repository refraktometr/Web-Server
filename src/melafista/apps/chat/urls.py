from django.conf.urls import patterns, include, url
from apps.chat import views


urlpatterns = patterns('apps.chat.views',
    url(r'^chat/$', views.chat),
    url(r'^chat/user/(\d+)/$', views.user_chat),
)
