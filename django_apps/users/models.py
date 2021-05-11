from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from datetime import timedelta, date


class User(AbstractUser):

    class Meta:
        db_table = '"users_users"'


# TODO
# review
# make migrations
# test
# commit
# create wrapper to get and validate token from the header for any secure endpoint
class AccessToken(models.Model):
    # Rules:
    # 1. users are only allowed one token at a time.
    # 2. records of tokens are note kept: tokens may be deleted once they have expired.
    # 3. tokens are not unique
    # 4. users are effectively unique: users are not unique at the db level,
    # but since we delete old user tokens before making new ones, users are
    # effectively unique for now.
    # 5. tokens should be retrieved using both user_id and token code since
    # codes are not unique.

    # Code should never contain sensitive data, encoded or otherwise,
    # since it will be stored locally on our mobile app.
    code = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)

    def generate(self, user_id):
        # Delete any access tokens already tied to user.
        AccessToken.objects.filter(user_id=user_id).delete()
        # Set user.
        self.user_id = user_id
        # Expiration date is one year from generation.
        self.expiration_date = timedelta(days=365)
        # Generate token: as of 2015, it is believed that 32 bytes (256 bits)
        # of randomness is sufficient for the typical use-case
        # expected for the secrets module.
        self.code = secrets.token_hex(60)

    def validate(self, user_id, code):
        if self.user_id != user_id:
            return False
        if self.code != code:
            return False
        if self.expiration_date <= date.today():
            return False
        return True

    def revoke(self):
        self.delete()

    class Meta:
        db_table = 'users_access_tokens'

    def __str__(self):
        return self.code
