from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.username)


class LoginTable(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.username)