# Generated by Django 3.2.3 on 2021-09-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_message_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(to='users.Users', verbose_name='Участник'),
        ),
    ]