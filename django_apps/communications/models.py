from django.db import models


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
    to_email = models.EmailField(
        verbose_name='To email',
        blank=False,
        null=False
    )
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    error = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'communications_emails'
