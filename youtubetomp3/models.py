from django.db import models
from django.contrib.auth.models import User

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.ForeignKey(User)

	@models.permalink
	def get_absolute_url(self):
		return ('profiles_profile_detail', (), { 'username': self.user.username })

	def __unicode__(self):
		return self.user.username
 
class Media(models.Model):
    user = models.ForeignKey(User)
    mediafile = models.FileField(upload_to='/media/')

    def __unicode__(self):
        return self.user.username + ": " + self.mediafile.url
