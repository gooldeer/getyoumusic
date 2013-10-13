from django.db import models
from django.contrib.auth.models import User

import os

import youtubetomp3.core.utils as Utils

# Create your models here.

class PlaylistManager(models.Manager):
    """PlaylistManager with checking on name"""
    def create_playlist(self, name, user, is_audio):
        if self.filter(name=name, user=user, is_audio=is_audio).count() != 0:
            return "DUBLICATE"
        else:
            return self.create(user=user, name=name, is_audio=is_audio)

class Playlist(models.Model):
    """Playlist which contains media objects"""

    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    is_audio = models.BooleanField(default=True)
    color = models.CharField(max_length=15, default='fff')
    objects = PlaylistManager()

    def __unicode__(self):
        return self.user.username + ": " + self.name

class MediaManager(models.Manager):
    """MediaManager with checking on name"""
    def create_media(self, playlist, mediafile):
        if self.filter(playlist=playlist, mediafile=mediafile).count() != 0:
            return "DUBLICATE"
        else:
            return self.create(playlist=playlist, mediafile=mediafile)    
        
class Media(models.Model):
    """Media files in playlist. Contains link on media file"""

    playlist = models.ForeignKey(Playlist)
    mediafile = models.CharField(max_length=50)
    objects = MediaManager()

    def __unicode__(self):
        return self.playlist.user.username + ": " + self.mediafile

    def delete(self):
        print self.mediafile

        os.remove(Utils.createPath(
            os.path.basename(self.mediafile), 
            self.playlist.user))
        
        super(Media, self).delete()


        
        
