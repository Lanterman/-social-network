# Generated by Django 3.2.3 on 2021-09-27 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_postsubscribers_escape'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-pub_date']},
        ),
    ]
