import unittest
SHA256_SECRET = "4468D9782DEF54FCD706C9100C71EC43932B1EBC2ACF6BA0560C05AAA7550C48"
SHA1_SECRET = "ASDFa34SDZCGSRT4534ad"
from adyen import Adyen


class Tests(unittest.TestCase):
    def test_sha256(self):
        data = {
            'merchantAccount': 'TestMerchant',
            'currencyCode': 'EUR',
            'paymentAmount': '199',
            'sessionValidity': '2015-06-25T10:31:06Z',
            'shipBeforeDate': '2015-07-01',
            'shopperLocale': 'en_GB',
            'merchantReference': 'SKINTEST-1435226439255',
            'skinCode': 'X7hsNDWp'
        }
        session = Adyen(data)
        session.settings.MERCHANT_SECRET = SHA256_SECRET
        session._set_signing_method('sha256')
        session.sign()
        self.assertEqual(
            session.data['merchantSig'], 'GJ1asjR5VmkvihDJxCd8yE2DGYOKwWwJCBiV3R51NFg=')

    def test_sha256_ignored_fields(self):
        data = {
            'merchantAccount': 'TestMerchant',
            'currencyCode': 'EUR',
            'paymentAmount': '199',
            'sessionValidity': '2015-06-25T10:31:06Z',
            'shipBeforeDate': '2015-07-01',
            'shopperLocale': 'en_GB',
            'merchantReference': 'SKINTEST-1435226439255',
            'skinCode': 'X7hsNDWp',
            # should not change the signature
            'ignore.me': 'test',
            'sig': 'test',
            'merchantSig': 'test',
        }
        session = Adyen(data)
        session.settings.MERCHANT_SECRET = SHA256_SECRET
        session._set_signing_method('sha256')
        session.sign()
        self.assertEqual(
            session.data['merchantSig'], 'GJ1asjR5VmkvihDJxCd8yE2DGYOKwWwJCBiV3R51NFg=')

    def test_sha1(self):
        data = {
            'address': 'sadasdf',
            'currencyCode': 'USD',
            'merchantAccount': 'ZazzyNL',
            'merchantReference': '9a3564af-744a-4b1b-b503-1fb339f752f0',
            'paymentAmount': 4465,
            'recurringContract': 'ONECLICK',
            'sessionValidity': '2015-12-01T16:53:01.947159+00:00',
            'shipBeforeDate': '2015-12-22T16:38:01.947141+00:00',
            'shopperEmail': 'anna+a@zazzy.me',
            'shopperLocale': 'en',
            'shopperReference': 'anna+a@zazzy.me',
            'skinCode': 'W7WasXf0'
        }
        session = Adyen(data)
        session.settings.MERCHANT_SECRET = SHA1_SECRET
        session._set_signing_method('sha1')
        session.sign()
        self.assertEqual(
            session.data['merchantSig'], 'LXLw+b3jEfUNsBLG3FYIj3teXkY=')

    def test_sha1_response(self):
        data = {
            'merchantReference': '9a3564af-744a-4b1b-b503-1fb339f752f0',
            'skinCode': 'W7WasXf0',
            'shopperLocale': 'en',
            'paymentMethod': 'visa',
            'authResult': 'AUTHORISED',
            'pspReference': 8514489882098740,
            'merchantSig': '08xZKJPwrAq9A/cNU6/Z3cFBB0E=',
        }
        session = Adyen(data)
        session.settings.MERCHANT_SECRET = SHA1_SECRET
        session._set_signing_method('sha1')
        self.assertTrue(session.is_valid())

        data['merchantSig'] = 'blah'
        session = Adyen(data)
        session.settings.MERCHANT_SECRET = SHA1_SECRET
        session._set_signing_method('sha1')
        self.assertFalse(session.is_valid())

    def test_sha256_response(self):
        MS = '2AFC1353849821D10CCF70A453CDC68FF54B71E099B916A6A30A52CECCCE8FF7'
        data = {
            'authResult': 'CANCELLED',
            'merchantReference': 'ab6bbd6d-dfb6-45b2-86f7-31b0b20d898a',
            'merchantSig': 'JmwOcrYh4H2W7mvSRUxSBcBROBfBcCLK/EhMGXboM78=',
            'shopperLocale': 'en',
            'skinCode': 'W7WasXf0',
            # should not be included:
            'merchantAccount': 'test',
        }
        session = Adyen(data)
        session.settings.MERCHANT_SECRET = MS
        session._set_signing_method('sha256')
        self.assertTrue(session.is_valid())

if __name__ == '__main__':
    unittest.main()
