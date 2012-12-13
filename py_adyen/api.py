from suds.client import Client
from py_adyen import settings as adyen_settings
# TODO: make this into seperate objects for payment/recurring?


class Api(object):
    def __init__(self, settings=adyen_settings):
        self.settings = settings

    def authorise_recurring_payment(self, reference, statement, amount, currency, shopper_reference, shopper_email, shopper_ip=None, recurring_detail_reference='LATEST'):
        assert statement != '', 'Statement is needed'
        assert reference != '', 'Reference is needed'
        assert shopper_reference != '', 'Shopper reference is needed'
        assert shopper_email != '', 'Shopper email is needed'
        assert currency != '', 'Currency is needed'
        assert int(amount) > 0, 'Amount is needed'

        payment = self.payment_service.factory.create('PaymentRequest')
        payment.shopperReference = shopper_reference
        payment.shopperEmail = shopper_email
        payment.recurring.contract = 'RECURRING'
        payment.merchantAccount = adyen_settings.MERCHANT_ACCOUNT
        payment.selectedRecurringDetailReference = recurring_detail_reference
        payment.amount.currency = currency
        payment.amount.value = amount
        payment.reference = reference
        payment.shopperInteraction = 'ContAuth'

        return self.payment_service.service.authorise(payment)

    @property
    def payment_service(self):
        # TODO: set test/production environment
        wsdl = 'https://pal-test.adyen.com/pal/Payment.wsdl'
        username = adyen_settings.API_USERNAME
        password = adyen_settings.API_PASSWORD
        client = Client(wsdl, username=username, password=password)
        return client

    @property
    def recurring_service(self):
        # TODO: set test/production environment
        wsdl = 'https://pal-test.adyen.com/pal/Recurring.wsdl'
        username = adyen_settings.API_USERNAME
        password = adyen_settings.API_PASSWORD
        client = Client(wsdl, username=username, password=password)
        return client
