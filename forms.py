from auctionapp.models import AuctionItem
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    #email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model=User
        fields = ['first_name','last_name','username','email','password1','password2']


class AuctionItemForm(forms.Form):
    CURRENCIES = {
        "EUR": "EUR",
        "USD": "USD",
        "PLN": "PLN",
    }
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1000)
    start_price = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=CURRENCIES)
    image = forms.ImageField()

class BidForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)