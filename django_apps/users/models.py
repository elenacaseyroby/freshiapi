from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.email

    class Meta:
        db_table = '"users_users"'

    def save(self, *args, **kwargs):
        # By default, username and email are unique but case sensitive.
        # To make sure that "Casey" and "casey" are treated the same,
        # we will make username and email lowercase before saving.
        self.username = self.username.lower()
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)
