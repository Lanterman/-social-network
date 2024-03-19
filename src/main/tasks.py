from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_message_about_group(group_name, group_slug, user_email):
    send_mail(
        f'You created the group "{group_name}"',
        f'To view you can follow the link \n http://127.0.0.1:8000/groups/{group_slug}/',
        'splen1011@mail.ru',
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_message_about_published(published_name, published_slug, user_email):
    send_mail(
        f'You created the publication "{published_name}"',
        f'To view you can follow the link \n http://127.0.0.1:8000/publish/{published_slug}/',
        'splen1011@mail.ru',
        [user_email],
        fail_silently=False,
    )
