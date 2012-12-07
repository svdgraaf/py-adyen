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

## TODO
Lots! Especially in the API section (only recurring payments are directly supported for now). Help out, make a pull request :)

*****
## Acknowledgement
Influenced by django-ogone, and reused some parts of the (outdated) django-adyen package