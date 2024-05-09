from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Articles(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='images')
    text = RichTextField(max_length=10000, default='Default')
    
    def __str__(self):
        return self.description

class Abonement(models.Model):
    TYPE_CHOICES = [
        ('заняття', 'Заняття'),
        ('місяці', 'Місяці'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    def __str__(self):
        return self.get_type_display()
    
    name = models.CharField(max_length=100)
    price = models.IntegerField(default='0')
    description = RichTextField(max_length=500, default='Default')
    
    def __str__(self):
        return self.name

  
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    abonement = models.ForeignKey(Abonement, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else 'Неавторизований користувач'
        return f'{username} - {self.abonement.name}'