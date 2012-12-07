from suds.client import Client
from adyen import settings as adyen_settings
# TODO: make this into seperate objects for payment/recurring?


class Api(object):
    def __init__(self, settings=adyen_settings):
        self.settings = settings

    def authorise_recurring_payment(self, reference, statement, amount, shopper, recurring_detail_reference='LATEST'):
        assert 'email' in shopper, 'Shopper has no email'
        assert 'reference' in shopper, 'Shopper has no reference'
        assert 'currency' in amount, 'Amount has no currency'
        assert 'value' in amount, 'Amount has no value'
        assert statement != '', 'Statement is needed'

        payment = self.payment_service.factory.create('PaymentRequest')
        payment.shopperReference = shopper['reference']
        payment.shopperEmail = shopper['email']
        payment.recurring.contract = 'RECURRING'
        payment.merchantAccount = adyen_settings.MERCHANT_ACCOUNT
        payment.selectedRecurringDetailReference = recurring_detail_reference
        payment.amount.currency = amount['currency']
        payment.amount.value = amount['value']
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
