# Generated by Django 2.2.9 on 2020-02-03 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='enables',
        ),
    ]
