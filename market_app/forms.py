from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment,Rate,Delivery, Grocery

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

                

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Add a comment...'

    class Meta:
        model = Comment
        fields = ('comment',)

        
class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        exclude = ['user']


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ['user', 'grocery']

class GroceryForm(forms.ModelForm):
    class Meta:
        model = Grocery
        exclude = ['date', 'discount_price']

class UpdateGroceryForm(forms.ModelForm):
    class Meta:
        model = Grocery
        exclude = ['date', 'discount_price', 'grocery_pic']
        exclude = ['user', 'grocerys']
