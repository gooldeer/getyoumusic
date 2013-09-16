from django.db import models
from django.contrib.auth.models import User
import os

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Create your models here.

class Media(models.Model):
    """Media files in playlist. Contains link on media file"""

    playlist = models.ForeignKey(Playlist)
    mediafile = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user.username + ": " + self.mediafile

    def delete(self):
    	print self.mediafile
    	os.remove(self.mediafile)
    	super(Media, self).delete()


class Playlist(models.Model):
    """Playlist which contains media objects"""

    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    is_audio = models.BooleanField(default=True)

    def __init__(self, arg):
        super(Playlist, self).__init__()
        self.arg = arg

    def __unicode__(self):
        return self.user.username + ": " + self.name
        
        
