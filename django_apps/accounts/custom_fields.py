from django.utils.deconstruct import deconstructible
from django.db.models import EmailField, CharField
from django.core.exceptions import ValidationError
from django.core import validators


@deconstructible
class CustomEmailValidator:
    message = "Enter a valid email address."
    code = "invalid"
    whitelist = "localhost"

    def __init__(self, message=None, code=None, whitelist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, value):
        # Check that email is at least 5 characters long: "x@x.x"
        if len(value) < 5:
            raise ValidationError(self.message, code=self.code)

        # Default email validator already checks that "@" is in email
        # (although I'm not sure what order the validators will be called in)
        # so this checks that the format is "x@x.x"
        if "@" in value:
            domain = value.split("@")[1]
            if "." not in domain:
                raise ValidationError(self.message, code=self.code)

        # Don't allow spaces.
        spaces = len(value.strip().split(" "))
        if spaces > 1:
            message = "Email cannot contain spaces."
            raise ValidationError(message, code=self.code)


custom_validate_email = CustomEmailValidator()


@deconstructible
class CustomUsernameValidator:
    message = None
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        # Check that username is at least 3 characters long.
        if len(value) < 3:
            message = "Username must be at least 3 characters in length."
            raise ValidationError(message, code=self.code)

        # Don't allow spaces.
        spaces = len(value.strip().split(" "))
        if spaces > 1:
            message = "Username cannot contain spaces."
            raise ValidationError(message, code=self.code)


custom_validate_username = CustomUsernameValidator()


class CustomEmailField(EmailField):
    default_validators = [validators.validate_email, custom_validate_email]

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs.setdefault('max_length', 254)
        super().__init__(*args, **kwargs)

    # Get value and set as lowercase.
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        value = value.lower().strip()
        return self.to_python(value)


class CustomUsernameField(CharField):
    validators = [custom_validate_username]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_length = 150
        self.validators.append(validators.MaxLengthValidator(max_length))

    # Get value and set as lowercase.
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        value = value.lower().strip()
        return self.to_python(value)
