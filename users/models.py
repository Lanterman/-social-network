from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from Sendji_004 import settings


class Users(AbstractUser):
    num_tel = models.CharField(max_length=20, verbose_name='Номер телефона')
    slug = models.SlugField(max_length=40, verbose_name='URL', blank=True)
    photo = models.ImageField(verbose_name='Фото', blank=True, upload_to='users/')
    friends = models.ManyToManyField('self', verbose_name='Друзья', related_name='friends_set', blank=True)
    email = models.EmailField('email address', blank=False)

    class Meta:
        ordering = ['first_name', 'last_name', 'username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('home', kwargs={'user_pk': self.pk})


class PostSubscribers(models.Model):
    owner = models.CharField(max_length=50, verbose_name='IP')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', max_length=50)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время заявки')
    escape = models.BooleanField(default=False, verbose_name='Просмотрел(-а)')

    class Meta:
        ordering = ['owner']
        verbose_name = 'Подтверждение'
        verbose_name_plural = 'Подтверждения'

    def __str__(self):
        return f'{self.owner} - {self.user}: {self.date}'


class Chat(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Участник")

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"

    def __str__(self):
        return f'{self.pk}'

    def get_absolute_url(self):
        return reverse('chat', kwargs={'chat_id': self.pk})


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    message = models.TextField("Сообщение", blank=True)
    pub_date = models.DateTimeField('Дата сообщения', auto_now_add=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ['pub_date']
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.message
