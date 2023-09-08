from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username

    username = models.CharField(max_length=30, unique=True)

    def save(self, *args, **kwargs): #TODO this bitch messes up the superuser
        if not self.is_staff:
            self.set_password(self.password)
            super().save()
        
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'