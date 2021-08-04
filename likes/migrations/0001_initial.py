# Generated by Django 3.2.3 on 2021-08-02 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0016_auto_20210802_1157'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Like')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время')),
                ('liked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Поставить лайк')),
                ('published', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.published', verbose_name='Публикация')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
            },
        ),
    ]
