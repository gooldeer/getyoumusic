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
    user = models.ForeignKey(User)
    mediafile = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user.username + ": " + self.mediafile

    def delete(self):
    	print self.mediafile
    	os.remove(self.mediafile)
    	super(Media, self).delete()
        
