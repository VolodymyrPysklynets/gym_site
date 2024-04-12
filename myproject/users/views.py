from django.shortcuts import render
from .forms import NewUserForm

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = NewUserForm()
    
    context = {
        'form':form
    }
    return render(request, 'users/register.html', context)
