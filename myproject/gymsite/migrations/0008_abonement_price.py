# Generated by Django 5.0.2 on 2024-03-29 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymsite', '0007_abonement'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonement',
            name='price',
            field=models.IntegerField(default='0'),
        ),
    ]
