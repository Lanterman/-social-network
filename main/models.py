from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import Users


class Abstract(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    slug = models.SlugField(error_messages={'unique': 'Такой URL уже существует!!!'},
                            help_text='<i>Заполняется автоматически!</i>', max_length=150, unique=True,
                            verbose_name='URL')
    biography = models.TextField(blank=True, verbose_name='Биография')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Published(Abstract):
    photo = models.ImageField(blank=True, upload_to='published/', verbose_name='Фото')
    date = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    owner = models.ForeignKey(Users, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True,
                              related_name='my_published')
    readers = models.ManyToManyField(Users, verbose_name='Читатель', through='UserPublishedRelation',
                                     related_name='published')
    group = models.ForeignKey('Groups', on_delete=models.CASCADE, verbose_name='Группа')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        db_table = 'Публикации'

    def get_absolute_url(self):
        return reverse('detail_publish', kwargs={'publish_slug': self.slug})


class Groups(Abstract):
    photo = models.ImageField(upload_to='groups/', verbose_name='Аватарка')
    users = models.ManyToManyField(Users, blank=True, related_name='groups_users', verbose_name='Пользователи')
    biography = None

    class Meta:
        ordering = ['name']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        db_table = 'Группы'

    def get_absolute_url(self):  # Вместо тега url и добавляет кнопку на страницу записи в админке
        return reverse('detail_group', kwargs={'group_slug': self.slug})


class Comments(Abstract):
    date = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    like = models.IntegerField(default=0, verbose_name='Лайки')
    published = models.ForeignKey(Published, on_delete=models.CASCADE, verbose_name='Публикация')
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    name, slug = None, None

    class Meta:
        ordering = ['-date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'Комментарии'

    def __str__(self):
        return self.published.name


class UserPublishedRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Не очень'),
        (2, 'Неплохая'),
        (3, 'Хорошая'),
        (4, 'Отличная'),
        (5, 'Всем советую'),
    )

    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    published = models.ForeignKey(Published, on_delete=models.CASCADE, verbose_name='Публикация')
    like = models.BooleanField(default=False, verbose_name='Like')
    in_mark = models.BooleanField(default=False, verbose_name='Закладки')
    rate = models.SmallIntegerField(verbose_name='Рейтинг', null=True, choices=RATE_CHOICES)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.user.username}: {self.published} - Рейтинг: {self.rate}'
