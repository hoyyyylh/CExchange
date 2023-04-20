from django.contrib import admin
from .models import Wallet, Exchange, Deposit, Complaint

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Exchange)
admin.site.register(Deposit)
admin.site.register(Complaint)