from django import forms

class loginUsForm(forms.Form):
   username = forms.CharField(required=False)
   password= forms.PasswordInput()