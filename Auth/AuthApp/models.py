from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    # one to one match from built in User from Django
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # additional

    # blank=true, users don't have to fill this out
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        # username is a default attribute of models.User
        return self.user.username
