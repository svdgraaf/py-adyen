from django import forms


class AdyenForm(forms.Form):
    """ Dynamic Adyen form """

    def __init__(self, initial_data, *args, **kwargs):
        super(AdyenForm, self).__init__(*args, **kwargs)
        for name, value in initial_data.items():
            self.fields[name] = forms.CharField(widget=forms.HiddenInput,
                initial=value)
