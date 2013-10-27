from django.conf.urls import patterns, url

from youtubetomp3 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^init_work/$', views.init_work, name="init_work"),
    url(r'^poll_state/$', views.poll_state, name="poll_state"),
    url(r'^playlists/$', views.playlists, name="playlists"),
    url(r'^new-playlist/$', views.new_playlist, name="new_playlist"),

    url(r'^playlists/remove/playlist=(?P<playlistName>[\w|\W]+),is_audio=(?P<is_audio>[\w|\W]+)/$', 
        views.remove_playlist, name="remove_playlist"),

    url(r'^playlists/(?P<playlistName>[\w|\W]+)/remove=(?P<media>[\w|\W]+)/$', 
        views.remove_media, name="remove_media"),
    url(r'^playlists/(?P<playlistName>[\w|\W]+)/update/name=(?P<name>[\w|\W]+);color=(?P<color>[\w|\W]+)/$', 
        views.change_playlist, name="change_playlist"),
    url(r'^playlists/(?P<playlistName>[\w|\W]+)/audio=(?P<media>[\w|\W]+);type=(?P<mediatype>[\w|\W]+)/$', views.audio, name="audio"),
    url(r'^playlists/(?P<playlist_name>[\w|\W]+)/add/media=(?P<media>[\w|\W]+)/$', 
        views.add_media_to_playlist, name="add_media_to_playlist"),
    url(r'^playlists/(?P<playlistName>[\w|\W]+)/$', views.playlist, name="playlist"),
    
    # url(r'^accounts/profile/$', views.profile, name="profile_detail"),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^profiles/', include('profiles.urls')),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'login': 'youtubetomp3/login.html'}),
)
