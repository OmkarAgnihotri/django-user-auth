from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from datetime import date
from .models import PasswordResets
import time

@shared_task
def send_email_verification_mail(user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    link = 'http://localhost:8000/auth/verify-email?'+'token='+str(user.verification_uuid)+'&email='+str(user.email)

    message = 'Follow this link to verify your account: '+ link
    send_mail(
        'Verify your account',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

@shared_task
def send_password_reset_mail(email,uid,token):
    
    link = 'http://localhost:8000/auth/password-reset/confirm?'+'uid='+uid+'&token='+token

    message = 'Follow this link to reset your password: '+ link

    send_mail(
        'Reset password',
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


@shared_task
def compute():
    sum = 0
    for i in range(10000000):
        sum+=i
        pass
    
    return sum
    