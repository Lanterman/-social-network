# Generated by Django 3.2.3 on 2021-08-11 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210811_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='like',
            field=models.BooleanField(default=False, verbose_name='Лайки'),
        ),
    ]