from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_registration_message(user_email):
    send_mail(
        f'Вы были зарегистрированы на нашем сайте',
        f'Вы были зарегистрированы на нашем сайте. Это рассылка, поэтому никаких действий не требуется.',
        'klivchinskydmitry@gmail.com',
        [user_email],
        fail_silently=False,
    )
