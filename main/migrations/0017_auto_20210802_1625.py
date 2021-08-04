# Generated by Django 3.2.3 on 2021-08-02 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_users_num_tel'),
        ('main', '0016_auto_20210802_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='published',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='published',
            name='like',
        ),
        migrations.AddField(
            model_name='published',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_published', to='users.users', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='groups',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='groups_users', to='users.Users', verbose_name='Пользователи'),
        ),
        migrations.CreateModel(
            name='UserPublishedRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Like')),
                ('in_mark', models.BooleanField(default=False, verbose_name='Закладки')),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 'Не очень'), (2, 'Неплохая'), (3, 'Хорошая'), (4, 'Отличная'), (5, 'Всем советую')], verbose_name='Рейтинг')),
                ('published', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.published', verbose_name='Публикация')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.AddField(
            model_name='published',
            name='readers',
            field=models.ManyToManyField(related_name='published', through='main.UserPublishedRelation', to='users.Users', verbose_name='Читатель'),
        ),
    ]
