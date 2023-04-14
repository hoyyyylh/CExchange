from django.db import models
from django.contrib.auth.models import User

CURRENCY = (('HKD',"HKD"),('BTC',"BTC"),('DASH',"DASH"),('DOGE',"DOGE"),('LTC',"LTC"))
SIDE = (('BUY',"BUY"),('SELL',"SELL"))

# Create your models here.
class Wallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=4, default="HKD", choices=CURRENCY)
    sec_key = models.CharField(max_length=255, null=True)
    pub_key = models.CharField(max_length=255, null=True)
    addr = models.CharField(max_length=255, null=True)
    balance = models.FloatField(default=0)

class Exchange(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=4, default="BTC", choices=CURRENCY)
    side = models.CharField(max_length=4, choices=SIDE)
    amount = models.FloatField(default=0)
    price = models.FloatField(default=0)
    done = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)
    taken_by = models.CharField(max_length=255, null=True)