# Generated by Django 5.0.2 on 2024-05-06 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_exercise_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='icon',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
