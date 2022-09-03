from django.forms import  ModelForm
from .models import Cart,Subscription,BillingAddress


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'quantity-text','id':'quantity', 'type':'number',
                                       'min':"1",
                                       'onfocus': 'if(this.value == "1") { this.value = ''; }',
                                        'onBlur':'if(this.value == '') { this.value = "1";}',
                                        'value':"1"})


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

    def __init__(self,*arg,**kwargs):
        super(SubscriptionForm, self).__init__(*arg,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'newsletter-input','placeholder':'Enter your email...'})


class BillingForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = '__all__'
        exclude = ['username', 'customer_id']

    def __init__(self,*arg,**kwargs):
        super(BillingForm, self).__init__(*arg,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})












