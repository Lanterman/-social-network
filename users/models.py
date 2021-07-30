from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

User._meta.get_field('email')._unique = True


class Users(User):
    num_tel = models.CharField(max_length=20, verbose_name='Номер телефона')
    slug = models.SlugField(max_length=100, verbose_name='URL', blank=True)
    photo = models.ImageField(verbose_name='Фото', blank=True, upload_to='users/')

    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     return reverse('profile', kwargs={'user_slug': self.slug})
