from django.db import models
from django.contrib.auth.models import User

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Create your models here.

class Media(models.Model):
    user = models.ForeignKey(User)
    mediafile = models.FileField(upload_to='/media/')

    def __unicode__(self):
        return self.user.username + ": " + self.mediafile.url
