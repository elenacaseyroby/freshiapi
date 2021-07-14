from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property


class Email(models.Model):
    # AbstractBaseUser provides the core implementation of a user model,
    # including hashed passwords and tokenized password resets.
    # AbstractUser provides authentication ^^ plus extra fields like
    # first_name, last_name, etc.
    from_email = models.EmailField(
        verbose_name='From email',
        blank=False,
        null=False
    )
    to_emails = ArrayField(
        models.EmailField(
            verbose_name='To email',
            blank=True
        ),
    )
    subject = models.CharField(max_length=255, null=True, blank=True)
    msg = models.TextField(null=True, blank=True)
    html_msg = models.TextField(null=True, blank=True)
    # time attempted to send
    sent_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    @cached_property
    def sent_successfully(self):
        if self.error:
            return False
        return True

    def __str__(self):
        return f"subject: '{self.subject}', to: {str(self.to_emails)}"

    class Meta:
        db_table = 'communications_emails'
