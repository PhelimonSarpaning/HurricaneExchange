# Generated by Django 2.2.4 on 2019-09-10 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0016_auto_20190910_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_history',
            name='share_price',
            field=models.FloatField(default=0.26),
            preserve_default=False,
        ),
    ]
