from django.urls import path
from .views import account, RegisterView, exercises, edit_plan, add_exercise_to_plan, remove_exercise_from_plan, update_quantity, update_exercise_order, save_temporary_plan, remove_temporary_exercise, update_temporary_quantity, delete_plan
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

app_name = "users"

urlpatterns = [
    path('account/', account, name='account'), 
    path('exercises/', exercises, name='exercises'), 
    path('edit_plan/', edit_plan, name='edit_plan'), 
    path('delete_plan/', delete_plan, name='delete_plan'),
    path('add_exercise_to_plan/', add_exercise_to_plan, name='add_exercise_to_plan'),
    path('remove_exercise_from_plan/', remove_exercise_from_plan, name='remove_exercise_from_plan'),
    path('save_temporary_plan/', save_temporary_plan, name='save_temporary_plan'),
    path('remove_temporary_exercise/', remove_temporary_exercise, name='remove_temporary_exercise'),
    path('update_temporary_quantity/', update_temporary_quantity, name='update_temporary_quantity'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('update_exercise_order/', update_exercise_order, name='update_exercise_order'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

