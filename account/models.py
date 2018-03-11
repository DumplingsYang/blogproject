from django.db import models
from django.contrib.auth.models import User
# Create your models here.


#Creat user account

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to = 'MEDIA_ROOT' , blank = True)
	def __str__(self):
		return self.user.username
