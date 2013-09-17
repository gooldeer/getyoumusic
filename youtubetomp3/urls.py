from django.conf.urls import patterns, include, url

from youtubetomp3 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^init_work/$', views.init_work, name="init_work"),
    url(r'^poll_state/$', views.poll_state, name="poll_state"),
    url(r'^playlist/$', views.media, name="media"),
    url(r'^playlist/new/$', views.new_playlist, name="new_playlist"),
    # url(r'^accounts/profile/$', views.profile, name="profile_detail"),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^profiles/', include('profiles.urls')),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'login': 'youtubetomp3/login.html'}),
)
