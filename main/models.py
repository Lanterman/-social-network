from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Abstract(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(error_messages={'unique': 'Такой URL уже существует!!!'},
                            help_text='<i>Заполняется автоматически!</i>', max_length=150, unique=True,
                            verbose_name='URL')
    biography = models.TextField(blank=True, verbose_name='Биография')

    class Meta:
        ordering = ['name']
        abstract = True

    def __str__(self):
        return self.name


class Published(Abstract):
    photo = models.ImageField(blank=True, upload_to='published/', verbose_name='Фото')
    date = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    like = models.IntegerField(default=0, verbose_name='Лайки')
    dislike = models.IntegerField(default=0, verbose_name='Дизлайки')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        db_table = 'Публикации'

    def get_absolute_url(self):
        return reverse('detail_publish', kwargs={'publish_slug': self.slug})


class Groups(Abstract):
    num_pub = models.IntegerField(default=0, verbose_name='Количество записей')
    photo = models.ImageField(blank=True, upload_to='groups/', verbose_name='Аватарка')
    published = models.ManyToManyField(Published, blank=True, verbose_name='Публикации')
    users = models.ManyToManyField(User, blank=True, related_name='+', verbose_name='Пользователи')
    biography = None

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        db_table = 'Группы'

    def get_absolute_url(self):  # Вместо тега url и добавляет кнопку на страницу записи в админке
        return reverse('detail_group', kwargs={'group_slug': self.slug})


class Comments(Abstract):
    date = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    like = models.IntegerField(default=0, verbose_name='Лайки')
    published = models.ForeignKey(Published, on_delete=models.CASCADE, verbose_name='Публикация')
    users = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name, slug = None, None

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'Комментарии'

    def __str__(self):
        return self.published.name
