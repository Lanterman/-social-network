# Generated by Django 3.2.3 on 2021-08-31 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_users_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='slug',
            field=models.SlugField(blank=True, max_length=40, verbose_name='URL'),
        ),
    ]
