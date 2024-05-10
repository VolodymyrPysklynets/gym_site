import uuid

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
    user_plans = UserExercisePlan.objects.filter(user=request.user).values('plan_id', 'plan_name').distinct()
    context = {'user_plans': user_plans}
    return render(request, 'users/account.html', context)

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
    plan_id = request.GET.get('plan_id')
    if request.method == 'POST':
        plan_name = request.POST.get('planname')
        if plan_id:
            plan_items = UserExercisePlan.objects.filter(user=request.user, plan_id=plan_id)
            for item in plan_items:
                item.plan_name = plan_name
                item.save()
        else:
            plan_id = uuid.uuid4()
            temp_plan = request.session.get('temp_plan', [])
            for item in temp_plan:
                exercise = Exercise.objects.get(id=item['exercise_id'])
                UserExercisePlan.objects.create(
                    user=request.user,
                    exercise=exercise,
                    plan_id=plan_id,
                    plan_name=plan_name,
                    quantity=1,
                    position=0
                )
            request.session.pop('temp_plan', None)
        return redirect('users:account')
    else:
        user_plan_items = []
        if plan_id:
            user_plan_items = UserExercisePlan.objects.filter(user=request.user, plan_id=plan_id).order_by('position').select_related('exercise')
            return render(request, 'users/edit_plan.html', {'user_plan_items': user_plan_items, 'plan_id': plan_id})
        else:
            temp_plan = request.session.get('temp_plan', [])
            user_plan_items = [{
                'id': "temp-" + str(index),
                'exercise_id': item['exercise_id'],
                'image_url': item['image_url'],
                'description': item['description'],
                'quantity': item.get('quantity', 1),
                'position': index
            } for index, item in enumerate(temp_plan)]
            return render(request, 'users/edit_plan_temporary.html', {'user_plan_items': user_plan_items})

@login_required
@require_POST
def add_exercise_to_plan(request):
    exercise_id = request.POST.get('exercise_id')
    if not exercise_id:
        return JsonResponse({'status': 'error', 'message': 'Invalid exercise ID'}, status=400)

    exercise = Exercise.objects.filter(id=exercise_id).first()
    if not exercise:
        return JsonResponse({'status': 'error', 'message': 'Exercise not found'}, status=404)

    temp_plan = request.session.get('temp_plan', [])
    temp_plan.append({
        'exercise_id': exercise.id,
        'description': exercise.description,
        'image_url': request.build_absolute_uri(exercise.image.url) if exercise.image else None,
        'icon_url': request.build_absolute_uri(exercise.icon.url) if exercise.icon else None
    })
    request.session['temp_plan'] = temp_plan

    return JsonResponse({'status': 'success', 'message': 'Exercise added to your plan.'})

@login_required
@require_POST
def remove_exercise_from_plan(request):
    plan_item_id = request.POST.get('plan_item_id')
    plan_id = request.POST.get('plan_id', None)

    if plan_id:
        try:
            plan_item = UserExercisePlan.objects.get(id=plan_item_id, plan_id=plan_id, user=request.user)
            plan_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Exercise removed from your plan.'})
        except UserExercisePlan.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Exercise not found in the plan.'}, status=404)
    else:
        temp_plan = request.session.get('temp_plan', [])
        temp_plan = [item for item in temp_plan if str(item['exercise_id']) != plan_item_id]
        request.session['temp_plan'] = temp_plan
        return JsonResponse({'status': 'success', 'message': 'Exercise removed from temporary plan.'})

@login_required
@require_POST
def update_quantity(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        plan_item_id = request.POST.get('plan_item_id')
        quantity = int(request.POST.get('quantity', 1))
        plan_id = request.POST.get('plan_id', None)

        if plan_id:
            try:
                plan_item = UserExercisePlan.objects.get(id=plan_item_id, user=request.user)
                plan_item.quantity = quantity
                plan_item.save()
                return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully.'})
            except UserExercisePlan.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Plan item not found.'}, status=404)
        else:
            temp_plan = request.session.get('temp_plan', [])
            for item in temp_plan:
                if str(item['exercise_id']) == plan_item_id:
                    item['quantity'] = quantity
                    break
            request.session['temp_plan'] = temp_plan
            return JsonResponse({'status': 'success', 'message': 'Temporary plan quantity updated successfully.'})

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

@login_required
@require_POST
def save_temporary_plan(request):
    plan_name = request.POST.get('planname')
    if not plan_name:
        return HttpResponse('Plan name is required', status=400)

    plan_id = uuid.uuid4()  
    temp_plan = request.session.get('temp_plan', [])

    for item in temp_plan:
        exercise = Exercise.objects.get(id=item['exercise_id'])
        UserExercisePlan.objects.create(
            user=request.user,
            exercise=exercise,
            plan_id=plan_id,
            plan_name=plan_name,
            quantity=item.get('quantity', 1),
            position=0
        )
    request.session.pop('temp_plan', None)  

    return redirect('users:account')  

@login_required
@require_POST
def remove_temporary_exercise(request):
    exercise_id = request.POST.get('exercise_id')
    if not exercise_id:
        return JsonResponse({'status': 'error', 'message': 'Exercise ID is required'}, status=400)

    temp_plan = request.session.get('temp_plan', [])
    temp_plan = [item for item in temp_plan if str(item['exercise_id']) != str(exercise_id)]
    request.session['temp_plan'] = temp_plan

    return JsonResponse({'status': 'success', 'message': 'Exercise removed successfully.'})

@login_required
@require_POST
def update_temporary_quantity(request):
    exercise_id = request.POST.get('exercise_id')
    new_quantity = int(request.POST.get('quantity', 1))  

    if not exercise_id:
        return JsonResponse({'status': 'error', 'message': 'Exercise ID is required'}, status=400)

    temp_plan = request.session.get('temp_plan', [])
    for item in temp_plan:
        if str(item['exercise_id']) == str(exercise_id):
            item['quantity'] = new_quantity
            break
    request.session['temp_plan'] = temp_plan

    return JsonResponse({'status': 'success', 'message': 'Quantity updated successfully.'})

@login_required
@require_POST
def delete_plan(request):
    plan_id = request.POST.get('plan_id')
    if not plan_id:
        return JsonResponse({'status': 'error', 'message': 'Plan ID is required'}, status=400)

    try:
        plan = UserExercisePlan.objects.filter(plan_id=plan_id, user=request.user)
        plan.delete()
        return JsonResponse({'status': 'success', 'message': 'Plan deleted successfully.'})
    except UserExercisePlan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Plan not found.'}, status=404)


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