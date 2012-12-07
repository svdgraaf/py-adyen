import logging
logger = logging.getLogger(__name__)

try:
    from django.conf import settings
except ImportError:
    # We do not need Django to used this package
    settings = {}

# Required settings
MERCHANT_ACCOUNT = getattr(settings, 'ADYEN_MERCHANT_ACCOUNT', None)
MERCHANT_SECRET = getattr(settings, 'ADYEN_MERCHANT_SECRET', None)

# Optional settings
ENVIRONMENT = getattr(settings, 'ADYEN_ENVIRONMENT', 'test')
API_USERNAME = getattr(settings, 'ADYEN_API_USERNAME', None)
API_PASSWORD = getattr(settings, 'ADYEN_API_PASSWORD', None)

DEFAULT_SKIN = getattr(settings, 'ADYEN_DEFAULT_SKIN', None)
ONE_PAGE = getattr(settings, 'ADYEN_ONE_PAGE', True)
