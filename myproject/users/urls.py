from django.urls import path
from .views import register, account, login_view

urlpatterns = [
    path('register/', register), 
    path('account/', account, name='account'), 
    path('login/', login_view, name='login'),
]

