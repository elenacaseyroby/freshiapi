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
    1. Users are allowed up to 5 active access tokens at a time.
    2. A token is active if the expiration_date is greater than the current date.
    3. Tokens are JWT tokens hashed with FRESHI_AUTH_ACCESS_KEY.
    They store the user_id and a code which will link back to a unique AccessToken record.  
    4. The code is not unique and could be reused in many users' access tokens.
    5. Tokens must be retrieved using both user_id and token code since
    codes alone are not unique.'''

    # Code adds complexity to access token, so we can't be hacked with
    # FRESHI_AUTH_ACCESS_KEY and user_id alone and also allows for
    # multiple active codes at once, for multiple devices.
    code = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    unique_together = [['user_id', 'code']]
    # The first element in each tuple is the actual value to be set
    # on the model, and the second element is the human-readable name.
    PURPOSE_CHOICES = (
        ('login', 'LOGIN'),
        ('pw_reset', 'PW_RESET'),
    )
    purpose = models.CharField(
        max_length=20, choices=PURPOSE_CHOICES, default='login')
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    def generate_token(self, user_id, purpose):
        '''Create access token object for user and return token.'''
        # Set user.
        self.user_id = user_id

        # Set expiration date based on purpose.
        if purpose == 'pw_reset':
            self.expiration_date = date.today() + relativedelta(hours=1)
            self.purpose = purpose
        else:
            self.expiration_date = date.today() + relativedelta(years=1)
            self.purpose = 'login'

        # Expiration date is one year from generation.

        # Get user's active tokens.
        active_tokens = AccessToken.objects.filter(
            user_id=user_id,
            # active
            expiration_date__gt=date.today()
        ).order_by('expiration_date').all()

        # If user has over the allowable number of active access tokens
        # revoke access for the oldest token.
        concurrent_logins_allowed = 5
        if active_tokens.count() >= concurrent_logins_allowed:
            oldest_token = active_tokens.first()
            oldest_token.revoke()

        # Create unique user_id / code combo for new access token.
        active_token_exists = True
        attempts = 0
        code = None
        while active_token_exists and attempts < 10:
            # generate new code until unique user_id / code combo is found.
            # kill after 10 attempts
            code = secrets.token_hex(60)[:100]
            active_token_exists = active_tokens.filter(
                code=code).exists()
            attempts += 1
        self.code = code
        self.save()

        return self.token

    @cached_property
    def is_active(self):
        return self.expiration_date > date.today()

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
        # Set expiration_date to today.
        self.expiration_date = date.today()
        self.save()

    class Meta:
        db_table = 'api_auth_access_tokens'

    def __str__(self):
        return self.code
