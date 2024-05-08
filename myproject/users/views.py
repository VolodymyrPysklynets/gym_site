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
    user_plan_items = UserExercisePlan.objects.filter(user=request.user).select_related('exercise').order_by('position')
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

@login_required
@require_POST  
def remove_exercise_from_plan(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        plan_item_id = request.POST.get('plan_item_id')
        try:
            plan_item = UserExercisePlan.objects.get(id=plan_item_id, user=request.user)
            plan_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Exercise removed from your plan.'})
        except UserExercisePlan.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Exercise not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@require_POST
def update_quantity(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        plan_item_id = request.POST.get('plan_item_id')
        quantity = int(request.POST.get('quantity', 1))
        try:
            plan_item = UserExercisePlan.objects.get(id=plan_item_id, user=request.user)
            plan_item.quantity = quantity
            plan_item.save()
            return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully.'})
        except UserExercisePlan.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Plan item not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@require_POST
def update_exercise_order(request):
    order = request.POST.get('order')
    if not order:
        return JsonResponse({'status': 'error', 'message': 'No order provided'}, status=400)

    try:
        item_ids = [int(id.strip()) for id in order.split(',')]
        for index, item_id in enumerate(item_ids):
            plan_item = UserExercisePlan.objects.get(id=item_id)
            plan_item.position = index
            plan_item.save()
        return JsonResponse({'status': 'success', 'message': 'Order updated successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error updating order: {str(e)}'}, status=500)


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