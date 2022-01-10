from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_message(user, chat_id):
    send_mail(
        f'Вам пришло сообщение от {user.first_name} {user.last_name}',
        f'Для просмотра сообщения можно перейти по ссылке \n http://127.0.0.1:8000/messages/chat/{chat_id}/',
        'klivchinskydmitry@gmail.com',
        ['klivchinskydmitry@gmail.com'],
        fail_silently=False,
    )
