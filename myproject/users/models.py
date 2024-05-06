from django.db import models

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


