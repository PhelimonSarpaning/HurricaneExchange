# Generated by Django 2.2.4 on 2019-10-03 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0020_transaction_history_trading_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='stock_dayChangePercent',
            field=models.CharField(default='10.0', max_length=20),
        ),
    ]
