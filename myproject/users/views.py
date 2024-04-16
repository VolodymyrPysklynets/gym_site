from django.shortcuts import render
from django.shortcuts import redirect
from .forms import NewUserForm

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = NewUserForm()
    
    context = {
        'form':form
    }
    return render(request, 'users/register.html', context)

def account(request):
    return render(request, 'users/account.html')