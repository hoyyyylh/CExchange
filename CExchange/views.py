from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .script import CreateAC, RefreshWallet, deal_confirm, getprice, gentoken, gentrans
from .models import Wallet, Exchange, Deposit, Complaint

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    price = getprice()
    context = {
        "price" : price
    }
    return HttpResponse(template.render(context,request))

def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))

def addrecord(request):
    x = request.POST['username']
    y = request.POST['password']
    z = request.POST['email']
    user = User.objects.create_user(x,z,y)
    user.save()
    CreateAC(user)
    return HttpResponseRedirect(reverse('index'))

def information(request):
    template = loader.get_template('information.html')
    return HttpResponse(template.render({}, request))

@login_required
def profile(request):
    template = loader.get_template('profile.html')
    mywallet = Wallet.objects.filter(owner=request.user)
    mybal = []
    for wallet in mywallet:
        if wallet.currency != "HKD":
            #RefreshWallet(wallet)
            word = str(wallet.currency) + ": " + str(wallet.balance)
            mybal.append(word)
        else:
            word = str(wallet.currency) + ": " + str(wallet.balance)
            mybal.append(word)
    
    context = {
        "mybal" : mybal,
    }
    return HttpResponse(template.render(context,request))

@login_required
def checkout_page(request):
    template = loader.get_template('checkout.html')

    braintree_client_token = gentoken()

    context = {'braintree_client_token': braintree_client_token}

    return HttpResponse(template.render(context,request))

@login_required
def payment(request):
    nonce_from_the_client = request.POST['payment_method_nonce']
    amount = request.POST['amount']

    result = gentrans(amount)

    if result.is_success:
        mywallet = Wallet.objects.filter(owner=request.user).get(currency="HKD")
        amount = float(amount)
        mywallet.balance += amount
        mywallet.save()
        newcharge = Deposit(owner=request.user, amount=amount)
        newcharge.save()
        return HttpResponseRedirect(reverse('success'))
    else:
        return HttpResponseRedirect(reverse('fatality'))

@login_required
def make_ex(request):
    template = loader.get_template('make_ex.html')
    return HttpResponse(template.render({}, request))

@login_required
def make_exchange(request):
    owner = request.user
    cur = request.POST['cur']
    side = request.POST['side']
    amount = request.POST['amount']
    price = request.POST['price']
    newexchange = Exchange(owner=owner,currency=cur,side=side,amount=amount,price=price)
    newexchange.save()
    return HttpResponseRedirect(reverse('my_ex'))

@login_required
def my_ex(request):
    template = loader.get_template('my_ex.html')
    myexchange = Exchange.objects.filter(owner=request.user).values()
    mydeposit = Deposit.objects.filter(owner=request.user).values()
    context = {
        'myexchange': myexchange,
        'mydeposit': mydeposit
    }
    return HttpResponse(template.render(context,request))

@login_required
def ex_list(request):
    template = loader.get_template('ex_list.html')
    exlist = Exchange.objects.exclude(owner=request.user).filter(done=False)
    for ex in exlist:
        if ex.side == "BUY":
            ownerwallet = Wallet.objects.filter(owner=ex.owner).get(currency="HKD")
            if ownerwallet.balance < ex.price:
                ex.dead = True
                ex.save()
            else:
                ex.dead = False
                ex.save()
        else:
            ownerwallet = Wallet.objects.filter(owner=ex.owner).get(currency=ex.currency)
            RefreshWallet(ownerwallet)
            if ownerwallet.balance < ex.amount:
                ex.dead = True
                ex.save()
            else:
                ex.dead = False
                ex.save()
    finalexlist = Exchange.objects.exclude(owner=request.user).filter(dead=False).filter(done=False).values()
    context = {
        'finalexlist' : finalexlist,
    }
    return HttpResponse(template.render(context,request))

@login_required
def confirm(request, id):
    template = loader.get_template('confirm.html')
    ex = Exchange.objects.get(id=id)
    context = {
        "ex" : ex,
    }
    return HttpResponse(template.render(context,request))

@login_required
def deal(request, id):
    user = request.user
    result = deal_confirm(id, user)
    if result == True:
        return HttpResponseRedirect(reverse('success'))
    else:
        return HttpResponseRedirect(reverse('fatality'))
    
@login_required
def complaint(request):
    template = loader.get_template('complaint.html')
    return HttpResponse(template.render({}, request))

@login_required
def addcomplaint(request):
    x = request.POST['complaint']
    user = request.user
    newcomplaint = Complaint(owner=user, messages=x)
    newcomplaint.save()
    return HttpResponseRedirect(reverse('success'))
    
def success(request):
    template = loader.get_template('success.html')
    return HttpResponse(template.render({}, request))

def fatality(request):
    template = loader.get_template('fatality.html')
    return HttpResponse(template.render({}, request))

@login_required
def complaintlist(request):
    if request.user.is_superuser:
        template = loader.get_template('complaintlist.html')
        complaint = Complaint.objects.all().values()
        context = {
            'complaint': complaint
        }
        return HttpResponse(template.render(context,request))
    else:
        return HttpResponseRedirect(reverse('index'))