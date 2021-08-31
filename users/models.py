from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

User._meta.get_field('email')._unique = True


class Users(User):
    num_tel = models.CharField(max_length=20, verbose_name='Номер телефона')
    slug = models.SlugField(max_length=40, verbose_name='URL', blank=True)
    photo = models.ImageField(verbose_name='Фото', blank=True, upload_to='users/')
    friends = models.ManyToManyField('self', verbose_name='Друзья', related_name='friends_set', blank=True)

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
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь', max_length=50)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время заявки')

    class Meta:
        ordering = ['owner']
        verbose_name = 'Подтверждение'
        verbose_name_plural = 'Подтверждения'

    def __str__(self):
        return f'{self.owner} - {self.user}: {self.date}'
