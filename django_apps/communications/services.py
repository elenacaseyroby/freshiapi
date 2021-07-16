from django.conf import settings
from rest_framework.response import Response
from django.core.mail import send_mail
from django_apps.communications.models import Email


# An in house function to send email, record email in communications_emails table
# and return response with status and detail message describing success or failure.
def send_email(subject, message, from_email, to_emails, html_message=None):
    # INPUT
    # subject string
    # message string
    # from_email email
    # to_emails list of emails
    # html_message

    # OUTPUT
    # response = {
    #   'status_code': int,
    #   'detail': str
    # }

    # Set if email fails to send
    email_error = None
    # Set if email fails to be recorded in db
    db_error = None

    # Send email
    try:
        send_mail(
            subject,
            message,
            from_email,
            to_emails,
            fail_silently=False,
            html_message=html_message)
    except Exception as e:
        email_error = f"Email failed to send: {str(e)}"

    # Record email
    try:
        email = Email()
        email.subject = subject
        email.msg = message
        email.html_msg = html_message
        email.from_email = from_email
        email.to_emails = to_emails
        email.error = email_error
        email.save()
    except Exception as e:
        db_error = f"Email failed to be recorded in communications_emails table: {str(e)}"

    # Return response
    if email_error:
        return {
            'status_code': 500,
            'detail': email_error
        }

    if db_error:
        return {
            'status_code': 200,
            'detail': db_error
        }

    return {
        'status_code': 200,
        'detail': 'Email successfully sent!'
    }
