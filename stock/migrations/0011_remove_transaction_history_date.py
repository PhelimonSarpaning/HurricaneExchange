# Generated by Django 2.2.4 on 2019-09-09 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_auto_20190909_0633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction_history',
            name='date',
        ),
    ]
