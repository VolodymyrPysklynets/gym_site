# Generated by Django 5.0.2 on 2024-05-06 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_exercise_type2_alter_exercise_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='type',
            field=models.CharField(choices=[('ноги', 'Ноги'), ('руки', 'Руки'), ('прес', 'Прес'), ('спина', 'Спина'), ('груди', 'Груди'), ('плечі', 'плечі')], max_length=20),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='type2',
            field=models.CharField(choices=[('з обладженням', 'З обладненням'), ('без обладнення', 'Без обладнення')], max_length=40, null=True),
        ),
    ]
