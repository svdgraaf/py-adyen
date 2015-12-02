import logging
logger = logging.getLogger(__name__)

try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    try:
        MERCHANT_ACCOUNT = getattr(settings, 'ADYEN_MERCHANT_ACCOUNT', None)
    except ImproperlyConfigured:
        logger.warning('Django settings are not configured')
        # if Django is available, but settings aren't configured
        settings = {}
except ImportError:
    # We do not need Django to used this package
    logger.warning('Django settings are not available')
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
SIGNING_METHOD = getattr(settings, 'ADYEN_SIGNING_METHOD', 'sha1').lower()
