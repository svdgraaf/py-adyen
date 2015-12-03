import logging
log = logging.getLogger(__name__)

import base64
import hmac
from hashlib import sha256, sha1
import binascii
from collections import OrderedDict

from decimal import Decimal
from datetime import datetime, date, timedelta

from urllib import urlencode
import re

import py_adyen.settings as adyen_settings
try:
    import py_adyen.forms as adyen_forms
except:
    # form not available
    pass


class Adyen(object):
    SHA1_SIGNATURE_FIELDS = (
        'paymentAmount', 'currencyCode', 'shipBeforeDate',
        'merchantReference', 'skinCode', 'merchantAccount',
        'sessionValidity', 'shopperEmail', 'shopperReference',
        'allowedMethods', 'blockedMethods', 'shopperStatement',
        'billingAddressType', 'recurringContract', 'billingAddressType',
        'deliveryAddressType',
    )
    SHA256_IGNORE_FIELDS_RE = re.compile('^(?:sig|merchantSig|ignore\..*)$')

    REQUIRED_FIELDS = frozenset((
        'merchantReference', 'paymentAmount', 'currencyCode',
        'shipBeforeDate', 'skinCode', 'merchantAccount', 'sessionValidity')
    )

    RESULT_REQUIRED_FIELDS = frozenset((
        'authResult', 'merchantReference', 'skinCode',
        'merchantSig', 'shopperLocale')
    )

    def __init__(self, data=None, settings=adyen_settings):
        # This allows us to override settings for the whole class
        self.settings = settings

        # set the target url according to the environment setting
        self.url = 'https://{}.adyen.com/hpp/'.format(adyen_settings.ENVIRONMENT)

        assert data, \
            'Please provide a set of data'

        # set the default skin
        if 'skinCode' not in data and self.settings.DEFAULT_SKIN:
            data['skinCode'] = self.settings.DEFAULT_SKIN

        # set the default merchant account
        if 'merchantAccount' not in data and self.settings.MERCHANT_ACCOUNT:
            data['merchantAccount'] = self.settings.MERCHANT_ACCOUNT

        self.data = data

        self._set_signing_method(self.settings.SIGNING_METHOD)

        # Make sure we convert any data from native Python formats to
        # the format required by Adyen.
        self.convert()

    def _set_signing_method(self, method):
        self.settings.SIGNING_METHOD = method
        if method == 'sha256':
            self.RESULT_SIGNATURE_FIELDS = (
                'authResult', 'merchantReference', 'merchantReturnData', 'paymentMethod',
                'pspReference', 'shopperLocale', 'skinCode'
            )
        else:
            self.RESULT_SIGNATURE_FIELDS = (
                'authResult', 'pspReference', 'merchantReference', 'skinCode',
                'merchantReturnData',
            )

    @classmethod
    def _convert_date(cls, value):
        """ Convert a given date to proper format. """

        if isinstance(value, date):
            return value.isoformat()

        return unicode(value)

    @classmethod
    def _convert_validity(cls, value):
        """
        Convert a given datetime to proper format. In this case, we'll act a
        little sneaky and convert the given datetime to UTC just ot be sure
        it gets interpreted in the right way.

        If the value is a timedelta, this is interpreted as a given amount of
        time from now.
        """

        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, timedelta):
            # Take the current moment and set hte microseconds to zero
            now = datetime.utcnow()
            now = now.replace(microsecond=0)

            new = now + value

            # Make sure we return the result in timezone 'Zulu' (=UTC), just
            # as in documentation.
            return new.isoformat() + 'Z'

        return unicode(value)

    @classmethod
    def _convert_amount(cls, amount):
        """ Convert a given amount to the proper format. """

        if isinstance(amount, Decimal):
            amount = amount.shift(Decimal('2')).to_integral()

        assert int(amount), 'Cannot case amount to integer'

        return unicode(amount)

    def _convert_field(self, field, converter):
        """ If existant, convert the given field or fields in self.data. """
        if field in self.data:
            self.data[field] = converter(self.data[field])

    def convert(self):
        """ Attempt to convert eligible elements from native Python types. """
        self._convert_field('paymentAmount', self._convert_amount)
        self._convert_field('shipBeforeDate', self._convert_date)
        self._convert_field('sessionValidity', self._convert_validity)

        # Make sure it's all unicode strings from here on
        for field in self.data.keys():
            self.data[field] = unicode(self.data[field])

    def _sign_plaintext(self, plaintext):
        """
        Sign the string `plaintext` with the shared secret using HMAC and
        encode the result as a base64 encoded string.

        Source: Adyen Python signature implementation example.
        """
        if self.settings.SIGNING_METHOD == 'sha1':
            hm = hmac.new(self.settings.MERCHANT_SECRET, plaintext, sha1)
            hm = base64.encodestring(hm.digest()).strip()
        else:
            hmac_key = binascii.a2b_hex(self.settings.MERCHANT_SECRET)
            hm = hmac.new(hmac_key, plaintext, sha256)
            hm = base64.b64encode(hm.digest())
        return hm

    def _data_to_plaintext(self, included_fields=[]):
        """
        Concatenate the specified `included_fields` from the `data` dictionary.
        When SHA256 is used and `included_fields` aren't specified,
            exclude ones that match excluding rule.
        See https://docs.adyen.com/pages/viewpage.action?pageId=5376964
        """
        if self.settings.SIGNING_METHOD == 'sha1':
            plaintext = ''
            for field in included_fields:
                plaintext += self.data.get(field, '').encode('utf-8')
        else:
            def _escape(val):
                return val.replace('\\', '\\\\').replace(':', '\\:')

            data = OrderedDict(
                sorted([(k, v) for k, v in self.data.items()
                        if not (included_fields and k not in included_fields
                                or self.SHA256_IGNORE_FIELDS_RE.match(k))
                        ], key=lambda t: t[0]))
            plaintext = ':'.join(map(_escape, data.keys() + data.values()))
        return plaintext

    def get_redirect_url(self):
        """
        Construct the redirect URL for starting a payment.
        """

        # Make sure a signature is present in the data
        assert 'merchantSig' in self.data, 'Please sign the data before using'
        params = urlencode(self.data)

        action_url = self.get_action()

        return action_url + '?' + params

    def get_action(self):
        if self.settings.ONE_PAGE:
            return self.url + 'pay.shtml'
        else:
            return self.url + 'select.shtml'

    def sign(self):
        """
        Add required signatures to the session data dictionary. The given
        dictionary is updated in-place.
        """

        data_fields = self.data.keys()

        # Make sure all required fields are filled in
        assert self.REQUIRED_FIELDS.issubset(data_fields), \
            'Not all required fields are set.'

        # Set the merchant signature in data
        if self.settings.SIGNING_METHOD == 'sha1':
            # signing string includes only these fields in specific order
            plaintext = self._data_to_plaintext(self.SHA1_SIGNATURE_FIELDS)
        else:
            # signing string includes all fields except ones matching SHA256_IGNORE_FIELDS_RE
            plaintext = self._data_to_plaintext()
        self.data['merchantSig'] = self._sign_plaintext(plaintext)

        # # See whether one of the billing address fields are set
        # # If so, calculate the billing address signature.
        # for address_field in self.ADDRESS_SIGNATURE_FIELDS:
        #     if address_field in data_fields:
        #         billing_plaintext = \
        #             self._data_to_plaintext(self.ADDRESS_SIGNATURE_FIELDS)
        #         self.data['billingAddressSig'] = \
        #             self._sign_plaintext(billing_plaintext)

        #         # No need to continue, we already calculated the signature
        #         # for all billing fields
        #         break

    def get_form(self, settings=adyen_settings):
        log.debug('Sending the following data to Adyen: %s', self.data)
        form = adyen_forms.AdyenForm(self.data)

        return form

    def is_valid(self):
        """
        Validate the data signature for a payment result. Returns True when
        the signature is valid, False otherwise.
        """

        data_fields = self.data.keys()

        # Make sure all expected fields are in the result
        assert self.RESULT_REQUIRED_FIELDS.issubset(data_fields), \
            'Not all expected fields are present.'

        plaintext = self._data_to_plaintext(self.RESULT_SIGNATURE_FIELDS)
        signature = self._sign_plaintext(plaintext)

        if not signature == self.data['merchantSig']:
            return False

        return True
