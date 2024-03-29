from django.db import models
from django.contrib.auth.models import User
import os

from youtubetomp3.const.constants import _Const
import youtubetomp3.core.utils as Utils

CONST = _Const()

class PlaylistManager(models.Manager):
    """PlaylistManager with checking on name"""
    def create_playlist(self, name, user, is_audio):
        if self.filter(name=name, user=user, is_audio=is_audio).count() != 0:
            return CONST.DUBLICATE
        else:
            return self.create(user=user, name=name, is_audio=is_audio)

class Playlist(models.Model):
    """Playlist which contains media objects"""

    class Meta:
        ordering = ['name']

    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    is_audio = models.BooleanField(default=True)
    color = models.CharField(max_length=15, default='fff')
    objects = PlaylistManager()

    def __unicode__(self):
        return self.user.username + ": " + self.name

    def get_default_playlist(self):
        """ Returns default playlist (video or audio) according to is_audio field """
        if self.is_audio:
            playlist_name = CONST.DEFAULT_AUDIO_PLAYLIST
        else:
            playlist_name = CONST.DEFAULT_VIDEO_PLAYLIST

        return Playlist.objects.get(
            user=self.user, name=playlist_name, is_audio=self.is_audio)

class MediaManager(models.Manager):
    """MediaManager with checking on name"""
    def create_media(self, playlist, name, link_to_play, link_to_load):

        if self.filter(playlist=playlist, 
            name=name,
            link_to_play=link_to_play, 
            link_to_load=link_to_load).count() != 0:
        
            return CONST.DUBLICATE
        else:
            return self.create(playlist=playlist, 
                name=name, 
                link_to_play=link_to_play, 
                link_to_load=link_to_load)    
        
class Media(models.Model):
    """Media files in playlist. Contains link on media file"""

    class Meta:
        ordering = ['name']

    playlist = models.ForeignKey(Playlist)
    name = models.CharField(max_length=50)
    link_to_play = models.CharField(max_length=50)
    link_to_load = models.CharField(max_length=50)
    objects = MediaManager()

    def __unicode__(self):
        return self.playlist.user.username + ": " + self.link_to_play

    def rename(self, newName):
        self.name = newName

        self.link_to_play = Utils.rename(
            os.path.basename(self.link_to_play), newName, self.playlist.user)
        self.link_to_load = Utils.rename(
            os.path.basename(self.link_to_load), newName, self.playlist.user)

        self.save()

    def delete(self):

        if (self.playlist.name == CONST.DEFAULT_AUDIO_PLAYLIST 
            or self.playlist.name == CONST.DEFAULT_VIDEO_PLAYLIST):

            os.remove(Utils.createPath(
                os.path.basename(self.link_to_play), 
                self.playlist.user))

            if self.link_to_play != self.link_to_load:
                os.remove(Utils.createPath(
                    os.path.basename(self.link_to_load), 
                    self.playlist.user))
        
        super(Media, self).delete()


        
        
