# Generated by Django 3.2.3 on 2021-08-04 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_published_readers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratingstar',
            options={'ordering': ['value'], 'verbose_name': 'Звезда Рейтинг', 'verbose_name_plural': 'Звезда Рейтинги'},
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='published',
            new_name='movie',
        ),
    ]
