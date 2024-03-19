from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_registration_message(user_email):
    send_mail(
        f'You have been registered on my website',
        f'You have been registered on my website. This is a newsletter, so no action is required.',
        'splen1011@mail.ru',
        [user_email],
        fail_silently=False,
    )
