from django.conf.urls import patterns, url

from youtubetomp3 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^init_work/$', views.init_work, name="init_work"),
    url(r'^poll_state/$', views.poll_state, name="poll_state"),
    url(r'^playlists/$', views.playlists, name="playlists"),
    url(r'^new-playlist/$', views.new_playlist, name="new_playlist"),
    url(r'^playlists/remove/(?P<playlistName>[\w|\W]+)/$', views.remove_playlist, name="remove_playlist"),
    url(r'^playlists/(?P<playlistName>[\w|\W]+)/remove/(?P<media>[\w|\W]+)/$', views.remove_media, name="remove_media"),
    url(r'^playlists/(?P<playlistName>[\w|\W]+)/$', views.playlist, name="playlist"),
    # url(r'^accounts/profile/$', views.profile, name="profile_detail"),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^profiles/', include('profiles.urls')),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'login': 'youtubetomp3/login.html'}),
)
