from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .models import Exercise, UserExercisePlan
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

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

@login_required
def edit_plan(request):
    user_plan_items = UserExercisePlan.objects.filter(user=request.user).select_related('exercise')
    context = {'user_plan_items': user_plan_items}
    return render(request, 'users/edit_plan.html', context)

@login_required
@require_POST  
def add_exercise_to_plan(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        exercise_id = request.POST.get('exercise_id')
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            plan, created = UserExercisePlan.objects.get_or_create(user=request.user, exercise=exercise)
            return JsonResponse({'status': 'success', 'message': 'Exercise added to your plan.'})
        except Exercise.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Exercise not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

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