# Generated by Django 2.2.4 on 2019-09-09 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_transaction_history_date_of_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_history',
            name='date_of_transaction',
            field=models.DateTimeField(),
        ),
    ]