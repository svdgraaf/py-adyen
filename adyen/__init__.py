# Be careful here, otherwise setup.py won't work
try:
    from django_ogone.ogone import Ogone, OgoneDirectLink
    __ALL__ = (Ogone, OgoneDirectLink)
except ImportError:
    pass
