from django.db import models
from django.utils.functional import cached_property
import secrets
import jwt
from datetime import date
from dateutil.relativedelta import relativedelta
from backend.settings import FRESHI_AUTH_ACCESS_KEY


# Made custom AccessToken so we could be sure no sensitive data would be stored in
# the token (since it will be vulnerable to leaks when stored locally on our mobile
# app) and to easily manage expiration_dates and access revokation from our backend.
class AccessToken(models.Model):
    ''' Rules:
    1. Users are only allowed one access token at a time.
    2. Records of tokens are not saved: tokens may be deleted once they have expired.
    3. Token codes are not unique.
    5. Access tokens are JWT tokens hashed with FRESHI_AUTH_ACCESS_KEY.
    They store user_id and code which will link back to a unique AccessToken record.
    4. Users are effectively unique, since we delete all of a user's tokens before creating
    a new token for said user. That said, users are not unique at the db level in case we
    ever want to support multiple active access tokens per user.
    5. Tokens must be retrieved using both user_id and token code since
    codes are not unique.'''

    code = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    unique_together = [['user_id', 'code']]

    def generate_token(self, user_id):
        '''Create access token object for user and return token.'''
        # Delete any access tokens already tied to user.
        AccessToken.objects.filter(user_id=user_id).delete()
        # Set user.
        self.user_id = user_id
        # Expiration date is one year from generation.
        self.expiration_date = date.today() + relativedelta(years=1)
        # Code adds complexity to access token, so we can't be hacked with
        # FRESHI_AUTH_ACCESS_KEY and user_id alone and also allows for a future in
        # which a user could have multiple active codes at once, for multiple devices.
        self.code = secrets.token_hex(60)[:100]
        self.save()
        return self.token

    @cached_property
    def token(self):
        '''Tokens are JWT tokens hashed with the FRESHI_AUTH_ACCESS_KEY \
            that store a unique combo of user_id and code that will link back to a unique \
            AccessToken object.'''

        # Notes:
        # 1. Don't store expiration date in JWT token.
        # We want the db to be the source of truth
        # for the expiration date, so that we can
        # change the date to revoke access.
        # 2. Token should
        # never contain sensitive data, encoded or otherwise,
        # since it will be stored locally on our mobile app.
        payload = {
            'user_id': self.user_id,
            'code': self.code
        }
        # These tokens are pretty secure because they must be made with the
        # FRESHI_AUTH_ACCESS_KEY and a code and user_id combination from an
        # active access token record in the db. So to fake one, you would
        # need a lot of data from diverse and secure parts of our
        # backend infrastructure. And if our security was compromised, you
        # could invalidate all active tokens by changing the
        # FRESHI_AUTH_ACCESS_KEY.
        # Note: We chose to use the HS256 signature because the same server that
        # creates the key, decodes the key. If we had another server decoding the
        # key, we would want to use the RS256 signature, so that if the key used to
        # decode tokens was exposed, it couldn't be used to create new tokens.
        return jwt.encode(payload, FRESHI_AUTH_ACCESS_KEY, algorithm="HS256")

    def revoke(self):
        # Note: Could also be revoked by changing expiration_date
        # if we ever wanted to keep records of our access tokens.
        self.delete()

    class Meta:
        db_table = 'api_auth_access_tokens'

    def __str__(self):
        return self.code
