from django.urls import path
from .views import account, RegisterView

app_name = "users"

urlpatterns = [
    path('account/', account, name='account'), 
    path('register/', RegisterView.as_view(), name='register'),
]

