from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_message_about_group(group_name, group_slug, user_email):
    send_mail(
        f'Вы создали группу {group_name}',
        f'Для просмотра можно перейти по ссылке \n http://127.0.0.1:8000/groups/{group_slug}/',
        'klivchinskydmitry@gmail.com',
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_message_about_published(published_name, published_slug, user_email):
    send_mail(
        f'Вы создали запись {published_name}',
        f'Для просмотра можно перейти по ссылке \n http://127.0.0.1:8000/publish/{published_slug}/',
        'klivchinskydmitry@gmail.com',
        [user_email],
        fail_silently=False,
    )
