# Generated by Django 3.2.3 on 2021-07-26 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_comments_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groups',
            name='num_pub',
        ),
    ]