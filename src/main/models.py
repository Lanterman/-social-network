from django.db import models
from django.urls import reverse
from django.utils import timezone

from config import settings


class Abstract(models.Model):
    name = models.CharField(max_length=40, verbose_name='name', unique=True)
    slug = models.SlugField(error_messages={'unique': 'This URL already exists!!!!'},
                            help_text='<i>Automatic filling!</i>', max_length=40, unique=True,
                            verbose_name='URL')
    biography = models.TextField(verbose_name='biography')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Publication(Abstract):
    photo = models.ImageField(blank=True, upload_to='publication/', verbose_name='Фото')
    date = models.DateTimeField(default=timezone.now, verbose_name='pub_date')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='my_publication'
    )
    group = models.ForeignKey('group', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        db_table = 'Publications'

    def get_absolute_url(self):
        return reverse('detail_publish', kwargs={'publish_slug': self.slug})


class Group(Abstract):
    photo = models.ImageField(upload_to='groups/', verbose_name='photo')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='groups_followers', verbose_name='followers')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='owner', on_delete=models.SET_NULL, null=True,
                              related_name='my_groups')
    biography = None

    class Meta:
        ordering = ['name']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        db_table = 'Groups'

    def get_absolute_url(self):  # Вместо тега url и добавляет кнопку на страницу записи в админке
        return reverse('detail_group', kwargs={'group_slug': self.slug})


class Comment(Abstract):
    date = models.DateTimeField(default=timezone.now, verbose_name='date')
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='likes', related_name='likes', blank=True)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name='publication')
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='user')
    name, slug = None, None

    class Meta:
        ordering = ['-id']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'Comments'

    def __str__(self):
        return self.publication_id.name

    def get_absolute_url(self):
        return reverse('comments', kwargs={'publish_slug': self.publication_id.slug})


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='rating', default=0)

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'
        ordering = ['-value']

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    ip = models.CharField('IP', max_length=150)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name='publication')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f'{self.star} - {self.publication_id}: {self.ip}'
