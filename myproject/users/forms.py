from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Введіть електронну пошту"}))
    
    username = forms.CharField(required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введіть юзернейм"}))
    
    password1 = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Введіть пароль"}))
    
    password2 = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Повторіть пароль"}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

