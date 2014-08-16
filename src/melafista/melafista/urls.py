from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'', include('apps.users.urls')),
    url(r'', include('apps.chat.urls')),
)
