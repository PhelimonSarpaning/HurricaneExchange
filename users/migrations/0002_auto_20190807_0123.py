# Generated by Django 2.2.4 on 2019-08-07 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trading_account',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Stock_Amount',
        ),
        migrations.DeleteModel(
            name='Trading_Account',
        ),
    ]
