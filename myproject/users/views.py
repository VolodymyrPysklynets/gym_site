from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.urls import reverse_lazy
# from django.contrib.auth import authenticate, login
# from .forms import NewUserForm, UserLoginForm

# def register(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             first_name = form.cleaned_data.get('first_name')
#             last_name = form.cleaned_data.get('last_name')
#             password = form.cleaned_data.get('password1')
#             authenticate_user(request, first_name, last_name, password)
#             return redirect('account')
#     else:
#         form = NewUserForm()
    
#     context = {
#         'form':form
#     }
#     return render(request, 'users/register.html', context)

# def authenticate_user(request, first_name, last_name, password):
#     user = authenticate(request, first_name=first_name, last_name=last_name, password=password)
#     if user is not None:
#         login(request, user)

# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data.get('first_name')
#             password = form.cleaned_data.get('password')
#             authenticate_user(request, first_name, None, password)  # Передаємо None для last_name
#             return redirect('account')
#     else:
#         form = UserLoginForm()
    
#     context = {
#         'form': form
#     }
#     return render(request, 'users/login.html', context)

@login_required
def account(request):
    return render(request, 'users/account.html')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("users:account")
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)