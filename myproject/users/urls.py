from django.urls import path
from .views import account, RegisterView, exercises, edit_plan, add_exercise_to_plan
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

app_name = "users"

urlpatterns = [
    path('account/', account, name='account'), 
    path('exercises/', exercises, name='exercises'), 
    path('edit_plan/', edit_plan, name='edit_plan'), 
    path('add_exercise_to_plan/', add_exercise_to_plan, name='add_exercise_to_plan'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

