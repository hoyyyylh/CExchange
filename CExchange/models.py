from django.db import models
from django.contrib.auth.models import User

CURRENCY = (('HKD',"HKD"),('BTC',"BTC"),('BCH','BCH'),('DASH',"DASH"),('LTC',"LTC"))
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
    init_date = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=4, default="BTC", choices=CURRENCY)
    side = models.CharField(max_length=4, choices=SIDE)
    amount = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    done = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)
    taken_by = models.IntegerField(default=0)
    deal_date = models.DateTimeField(null=True)
    Txid = models.CharField(max_length=255, null=True)

class Deposit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

class Complaint(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.TextField(default="Just to Say Hi")
    date = models.DateTimeField(auto_now_add=True)