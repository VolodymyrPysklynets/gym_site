from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .models import Exercise
from django.http import JsonResponse
from django.template.loader import render_to_string

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

def exercises(request):
    equipment_types = request.GET.getlist('equipment_type[]')
    exercise_types = request.GET.getlist('exercise_type[]')
    
    items = Exercise.objects.all()
    if equipment_types:
        items = items.filter(type2__in=equipment_types)
    if exercise_types:
        items = items.filter(type__in=exercise_types)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string(
            'users/includes/exercise_list.html',
            {'items': items}
        )
        return JsonResponse({'html': html})
    
    context = {'items': items}
    return render(request, 'users/exercises.html', context)

def edit_plan(request):
    return render(request, 'users/edit_plan.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'