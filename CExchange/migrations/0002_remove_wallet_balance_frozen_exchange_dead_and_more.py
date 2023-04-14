# Generated by Django 4.1.7 on 2023-04-12 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CExchange', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='balance_frozen',
        ),
        migrations.AddField(
            model_name='exchange',
            name='dead',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='currency',
            field=models.CharField(choices=[('HKD', 'HKD'), ('BTC', 'BTC'), ('DASH', 'DASH'), ('DOGE', 'DOGE'), ('LTC', 'LTC')], default='BTC', max_length=4),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='side',
            field=models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=4),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=models.CharField(choices=[('HKD', 'HKD'), ('BTC', 'BTC'), ('DASH', 'DASH'), ('DOGE', 'DOGE'), ('LTC', 'LTC')], default='HKD', max_length=4),
        ),
    ]
