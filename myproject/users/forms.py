from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Введіть своє ім'я"}))
    last_name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введіть своє прізвище"}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Введіть електронну пошту"}))
    TYPE_CHOICES = [
        ('чоловік', 'Чоловік'),
        ('жінка', 'Жінка'),
        ('не бінарний', 'Не бінарний'),
    ]
    gender = forms.ChoiceField(choices=TYPE_CHOICES)
    
    password1 = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Введіть пароль"}))
    password2 = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Повторіть пароль"}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'gender', 'password1', 'password2')