# Generated by Django 3.2.3 on 2021-08-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210802_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpublishedrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Не очень'), (2, 'Неплохая'), (3, 'Хорошая'), (4, 'Отличная'), (5, 'Всем советую')], null=True, verbose_name='Рейтинг'),
        ),
    ]