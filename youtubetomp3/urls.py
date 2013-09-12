from django.conf.urls import patterns, url

from youtubetomp3 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^init_work/$', views.init_work, name="init_work"),
    url(r'^poll_state/$', views.poll_state, name="poll_state"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'login': 'youtubetomp3/login.html'}),
)
