from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['user','first_name','last_name','phone_number','email','address','zip_code']

        
    def __init__(self, request=None, *args, **kwargs):
        self.user = kwargs.pop('user','')
        super(OrderCreateForm, self).__init__(*args, **kwargs) # 꼭 있어야 한다!



