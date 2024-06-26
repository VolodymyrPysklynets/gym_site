import uuid
from django.db import models
from django.conf import settings

class Exercise(models.Model):
    TYPE_CHOICES = [
        ('ноги', 'Ноги'),
        ('руки', 'Руки'),
        ('прес', 'Прес'),
        ('спина', 'Спина'),
        ('груди', 'Груди'),
        ('плечі', 'плечі'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    def __str__(self):
        return self.get_type_display()
    
    TYPE2_CHOICES = [
        ('з обладженням', 'З обладненням'),
        ('без обладнення', 'Без обладнення'),
    ]
    type2 = models.CharField(max_length=40, choices=TYPE2_CHOICES, null=True)
    def __str__(self):
        return self.get_type2_display()
    
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='images')
    icon = models.ImageField(blank=True, upload_to='images')
    
    def __str__(self):
        return self.description

class UserExercisePlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    position = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    plan_name = models.CharField(max_length=100, null=True, blank=True)
    plan_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.user.username} - {self.plan_name} - {self.exercise.description} - {self.quantity}'

