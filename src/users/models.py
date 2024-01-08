from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from config import settings


class User(AbstractUser):
    """Customer user class"""

    num_tel: str = models.CharField(max_length=20, verbose_name='Номер телефона')
    slug: str = models.SlugField(max_length=40, verbose_name='URL', blank=True)
    photo: bytes = models.ImageField(verbose_name='Фото', blank=True, upload_to='users/')
    email: str = models.EmailField('email address', blank=False)

    class Meta:
        ordering = ['first_name', 'last_name', 'username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('home', kwargs={'user_pk': self.pk})


class Follower(models.Model): #  Сделать в первую очередь. Переписать логику друзей на подписчиков и подписки.
    """User followers"""

    follower_id: int = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, max_length=255, related_name="subscriptions")
    subscription_id: int = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, max_length=255, related_name="followers")
    date: datetime = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    is_checked: bool = models.BooleanField(default=False, verbose_name='Checked')

    class Meta:
        ordering = ['date']
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'

    def __str__(self):
        return f'{self.follower_id} - {self.subscription_id}: {self.date}'


class Chat(models.Model):
    """Chat with user"""

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="members")

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

    def __str__(self):
        return f'{self.pk}'

    def get_absolute_url(self):
        return reverse('chat', kwargs={'chat_id': self.pk})


class Message(models.Model):
    """User message for chat"""

    chat_id: int = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE)
    author_id: int = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Author", on_delete=models.CASCADE)
    message: str = models.TextField("Message", blank=True)
    pub_date: datetime = models.DateTimeField('Date', auto_now_add=True)
    is_readed: bool = models.BooleanField('Is read', default=False)

    class Meta:
        ordering = ['pub_date']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message
