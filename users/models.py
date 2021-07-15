from django.contrib.auth.models import User
from django.db import models


class Users(User):
    num_tel = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True)
    slug = models.SlugField(max_length=100, verbose_name='URL', blank=True)
    photo = models.ImageField(verbose_name='Фото', blank=True, upload_to='users/')

    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
