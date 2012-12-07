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
Please see the wiki for [usage examples](https://github.com/svdgraaf/py-adyen/wiki)


## TODO
Lots! Especially in the API section (only recurring payments are directly supported for now). Help out, make a pull request :)

*****
## Acknowledgement
Influenced by [django-ogone](https://github.com/tschellenbach/Django-ogone), and reused some parts of the (outdated) [django-adyen](https://github.com/dokterbob/django-adyen) package