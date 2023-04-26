# Generated by Django 4.1.7 on 2023-04-11 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('HKD', 'HKD'), ('LTC', 'LTC'), ('DASH', 'DASH'), ('DOGE', 'DOGE'), ('BTC', 'BTC')], default='HKD', max_length=4)),
                ('sec_key', models.CharField(max_length=255, null=True)),
                ('pub_key', models.CharField(max_length=255, null=True)),
                ('addr', models.CharField(max_length=255, null=True)),
                ('balance', models.FloatField(default=0)),
                ('balance_frozen', models.FloatField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('HKD', 'HKD'), ('LTC', 'LTC'), ('DASH', 'DASH'), ('DOGE', 'DOGE'), ('BTC', 'BTC')], default='BTC', max_length=4)),
                ('side', models.CharField(choices=[('B', 'BUY'), ('S', 'SELL')], max_length=4)),
                ('amount', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('done', models.BooleanField(default=False)),
                ('taken_by', models.CharField(max_length=255, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]