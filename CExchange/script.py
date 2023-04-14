from cryptos import *
import blockcypher
import braintree
import ccxt
from CryptoEx import settings
from .models import Wallet, Exchange

def CreateAC(user):
    name = user.username
    input_str = "I Love Rock and Roll" + name
    new_wallet1 = Wallet(owner=user, currency="HKD")
    new_wallet1.save()
    c2 = Bitcoin(testnet=True)
    priv = sha256(input_str)
    pub = c2.privtopub(priv)
    addr = c2.pubtoaddr(pub)
    new_wallet2 = Wallet(owner=user, currency="BTC", sec_key=priv, pub_key=pub, addr=addr)
    new_wallet2.save()
    c3 = Litecoin()
    priv = sha256(input_str)
    pub = c3.privtopub(priv)
    addr = c3.pubtoaddr(pub)
    new_wallet3 = Wallet(owner=user, currency="LTC", sec_key=priv, pub_key=pub, addr=addr)
    new_wallet3.save()
    c4 = Dash()
    priv = sha256(input_str)
    pub = c4.privtopub(priv)
    addr = c4.pubtoaddr(pub)
    new_wallet4 = Wallet(owner=user, currency="DASH", sec_key=priv, pub_key=pub, addr=addr)
    new_wallet4.save()
    c5 = Doge()
    priv = sha256(input_str)
    pub = c5.privtopub(priv)
    addr = c5.pubtoaddr(pub)
    new_wallet5 = Wallet(owner=user, currency="DOGE", sec_key=priv, pub_key=pub, addr=addr)
    new_wallet5.save()

def GetBal(addr, CUR):
    if CUR == "BTC":
        coin_symbol = 'btc-testnet'
    elif CUR == "LTC":
        coin_symbol = 'ltc'
    elif CUR == "DASH":
        coin_symbol = 'dash'
    elif CUR == "DOGE":
        coin_symbol = 'doge'
    bal = blockcypher.get_total_balance(addr, coin_symbol=coin_symbol)
    return bal

def RefreshWallet(wallet):
    newbal = GetBal(wallet.addr,wallet.currency)
    wallet.balance = newbal
    wallet.save()

def deal_confirm(id, user):
    ex = Exchange.objects.get(id=id)
    if ex.currency == "BTC":
        coin_symbol = 'btc-testnet'
    elif ex.currency == "LTC":
        coin_symbol = 'ltc'
    elif ex.currency == "DASH":
        coin_symbol = 'dash'
    elif ex.currency == "DOGE":
        coin_symbol = 'doge'
    result = True
    if ex.side == "BUY":
        targetwallet = Wallet.objects.filter(owner=user).get(currency=ex.currency)
        RefreshWallet(targetwallet)

        if targetwallet.balance < ex.amount:
            result = False
            return result
        
        ownerwallet = Wallet.objects.filter(owner=ex.owner).get(currency=ex.currency)
        amount = int(ex.amount)
        blockcypher.simple_spend(from_privkey=targetwallet.sec_key,to_address=ownerwallet.addr,to_satoshis=amount,coin_symbol=coin_symbol,api_key=settings.BLOCKCYPHER_TOKEN,privkey_is_compressed=False)
        RefreshWallet(targetwallet)
        RefreshWallet(ownerwallet)

        ownercash = Wallet.objects.filter(owner=ex.owner).get(currency="HKD")
        ownercash.balance -= ex.price
        ownercash.save()
        targetcash = Wallet.objects.filter(owner=user).get(currency="HKD")
        targetcash.balance += ex.price
        targetcash.save()
        ex.done = True
        ex.save()
    else:
        targetcash = Wallet.objects.filter(owner=user).get(currency="HKD")

        if targetcash.balance < ex.price:
            result = False
            return result
        
        targetwallet = Wallet.objects.filter(owner=user).get(currency=ex.currency)
        ownerwallet = Wallet.objects.filter(owner=ex.owner).get(currency=ex.currency)
        amount = int(ex.amount)
        blockcypher.simple_spend(from_privkey=ownerwallet.sec_key,to_address=targetwallet.addr,to_satoshis=amount,coin_symbol=coin_symbol,api_key=settings.BLOCKCYPHER_TOKEN,privkey_is_compressed=False)
        RefreshWallet(targetwallet)
        RefreshWallet(ownerwallet)

        ownercash = Wallet.objects.filter(owner=ex.owner).get(currency="HKD")
        ownercash.balance += ex.price
        ownercash.save()
        targetcash.balance -= ex.price
        targetcash.save()
        ex.done = True
        ex.save()
    return result

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
    braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY,
    )
)

def gentoken():
    braintree_client_token = gateway.client_token.generate({})
    return braintree_client_token

def gentrans(amount):
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": 'fake-valid-no-billing-address-nonce',
        "options": {
            "submit_for_settlement": True
        }
    })
    return result

exchange = ccxt.binance({
    'apiKey': settings.CCXT_APIKEY,
    'secret': settings.CCXT_SECKEY,
    'enableRateLimit': True,
})

exchange.set_sandbox_mode(True)

def getprice():
    price=[]
    word = "BTC: "
    ex = exchange.fetch_ticker('BTC/USD')['average']
    hkdp = float(ex)*7.85
    final = word + str(hkdp)
    price.append(final)
    word = "LTC: "
    ex = exchange.fetch_ticker('LTC/USD')['average']
    hkdp = float(ex)*7.85
    final = word + str(hkdp)
    price.append(final)
    word = "DASH: "
    ex = ex = exchange.fetch_ticker('DASH/USDT')['average']
    hkdp = float(ex)*7.85
    final = word + str(hkdp)
    price.append(final)
    word = "DOGE: "
    ex = exchange.fetch_ticker('DOGE/USD')['average']
    hkdp = float(ex)*7.85
    final = word + str(hkdp)
    price.append(final)
    return price