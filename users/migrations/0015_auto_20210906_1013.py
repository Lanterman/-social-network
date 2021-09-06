# Generated by Django 3.2.3 on 2021-09-06 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_postsubscribers_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsubscribers',
            name='owner',
            field=models.CharField(max_length=50, verbose_name='IP'),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.CharField(max_length=50, verbose_name='Отправитель')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('is_reading', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('to_user', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='users.users', verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['date'],
            },
        ),
    ]
