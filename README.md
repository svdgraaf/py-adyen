# py-adyen

Adyen Python implementation

## Installation

Install via pip:
```bash
$ pip install https://github.com/svdgraaf/py-adyen/archive/master.zip
```

## Requirements

Hmac, hashlib. If you want to use the API, you need Suds.

## Settings

These options are required:
* `ADYEN_MERCHANT_ACCOUNT`: Your Adyen Merchant account name
* `ADYEN_MERCHANT_SECRET`: Your Adyen shared secret

And optional:
* `ADYEN_DEFAULT_SKIN`: Either provide a skin with every payment data, or use this setting
* `ADYEN_ONE_PAGE`: Use Adyens One Page payment? (defaults to True)
* `ADYEN_ENVIRONMENT`: Defaults to 'test'
* `ADYEN_API_USERNAME`: Used for recurring payments (WS user for SOAP)
* `ADYEN_API_PASSWORD`: Password for your WS user (for SOAP)

*****
Py-adyen will try to fetch those settings from your Django settings "It Just Works(tm)". But you can always provide your own settings upon initialising of the Adyen instance, eg:

```python
from py_adyen.adyen import Adyen
a = Adyen(settings={})
```

## Usage

### Standard payments

```python
from py_adyen.adyen import Adyen
data = {
    'merchantReference': '1337',           # your internal reference for this payment
    'paymentAmount': 100,                  # amount in cents
    'currencyCode': 'EUR',                 # currency, in the 3 letter format (see Adyen docs)
    'shipBeforeDate': datetime.now(),      # useful for lookups (I guess)
    'shopperEmail': 'foobar@example.com',  # useful for recurring payments etc.
    'shopperReference': 'user-42',         # your internal reference for (recurring) lookups etc.
    'sessionValidity': datetime.now(),     # how long is the payment session valid
}

a = Adyen(data)
a.sign()
form = a.get_form()

print form                  # form with hidden items
print a.get_action()        # action url for the form
print a.get_redirect_url()  # useable for redirecting (uses GET args)
```

After the user is redirect back, you can use the is_valid() method for checking whether the data is valid. It is advised to use the fields from the Adyen notifications though.

```python
from py_adyen.adyen import Adyen
data = request.POST.dict()
a = Adyen(data)
a.is_valid()  # True when the signature is valid, False if not
```

### Recurring payments
** Make sure that your account is enabled for recurring payments, as this will otherwise not work **

The recurring payments is divided in 3 steps.
* Step 1 is to have the client authorise the first payment, you send a special field with the payment to mark it for recurrence
* Step 2 is to validate the authorisation (via the regular validation)
* Step 3 when a next payment is due, use the api to authorise a new payment, using the details from step 1

#### Step 1
Step 1 is roughly the same as the regular step. For a recurring payment, you will need to provided these fields:

```python
data = data + {
    'shopperEmail': request.user.email,   # 
    'shopperReference': request.user.id,  # Needs to be unique, you'll need this in step 3
    'recurringContract': 'RECURRING',     # Mark this authorisation for recurring payments
}
```

#### Step 2
Step is the validation step, make sure the authorisation is approved (via either the redirect data, or the notification). For your reference, it is advised to also store the psp data, as you might need it in the future. This is the last step in which the user is needed.

#### Step 3
When a new payment is due, call the Adyen api with the used data in step 1:

```python
from py_adyen.api import Api
ws = Api()

reference = 'order445'                  # internatl reference
statement = 'Subscription Fee October'  # public payment statement for user
amount = {'currency': 'EUR', 'value': 100}
shopper = {
    'email': 'foobar@example.com',
    'reference': 'user-42',             # Make sure this is the same as in step 1
    # 'ip': '127.0.0.1',                # Optional last used ip information, used in some fraud detection
}

ws.authorise_recurring_payment(reference, statement, amount, shopper, recurring_detail_reference='LATEST')

# (PaymentResult){
#    additionalData = None
#    authCode = None
#    dccAmount = None
#    dccSignature = None
#    fraudResult = None
#    issuerUrl = None
#    md = None
#    paRequest = None
#    pspReference = "xyz"
#    refusalReason = None
#    resultCode = "Received"  # The resultCode will vary
#  }
```
It is advised to store the result data (eg: pspReference) for future reference.

## TODO
Lots! Especially in the API section (only recurring payments are directly supported for now). Help out, make a pull request :)

*****
## Acknowledgement
Influenced by [django-ogone](https://github.com/tschellenbach/Django-ogone), and reused some parts of the (outdated) [django-adyen](https://github.com/dokterbob/django-adyen) package