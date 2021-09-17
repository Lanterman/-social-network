from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import Users


class Abstract(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название', unique=True)
    slug = models.SlugField(error_messages={'unique': 'Такой URL уже существует!!!'},
                            help_text='<i>Заполняется автоматически!</i>', max_length=40, unique=True,
                            verbose_name='URL')
    biography = models.TextField(verbose_name='Биография')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Published(Abstract):
    photo = models.ImageField(blank=True, upload_to='published/', verbose_name='Фото')
    date = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    owner = models.ForeignKey(Users, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True,
                              related_name='my_published')
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
    owner = models.ForeignKey(Users, verbose_name='Создатель группы', on_delete=models.SET_NULL, null=True,
                              related_name='my_group')
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
    like = models.ManyToManyField(Users, verbose_name='Лайки', related_name='likes')
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

    def get_absolute_url(self):
        return reverse('comments', kwargs={'publish_slug': self.published.slug})


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Звезда Рейтинг'
        verbose_name_plural = 'Звезда Рейтинги'
        ordering = ['-value']

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    ip = models.CharField('Пользователь', max_length=150)
    published = models.ForeignKey(Published, on_delete=models.CASCADE, verbose_name='Публикация')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.star} - {self.published}: {self.ip}'
