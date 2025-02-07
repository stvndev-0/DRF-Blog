from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

@shared_task
def reset_password(uidb64, token, email):
    url = reverse(
        'password-reset-confirm',
        kwargs={
            'uidb64': uidb64,
            'token': token
        }
    )
    full_url = settings.HOST + url

    message = f'Forgotten password, please click on this link {full_url} and enter a new password.'
    send_mail(
        subject='Reset your password',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

@shared_task
def verify_account(uidb64, token, email):
    url = reverse(
        'activation-email',
        kwargs={
            'uidb64': uidb64,
            'token': token
        }
    )
    verification_url = settings.HOST + url

    message = f'Click on this link {verification_url} to verify your email.'
    send_mail(
        subject='Verify your email',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

@shared_task
def unverified_account():
    time_limit = now() - timedelta(minutes=10)
    del_user = User.objects.filter(verified=False, date_joined__lte=time_limit)
    del_user.delete()