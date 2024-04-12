from django.shortcuts import render
from django.http import HttpResponse
from .models import Articles, Abonement

def index(request):
    return render(request, "gymsite/mainpage.html")

def base(request):
    return render(request, "gemsite/base.html")

def grouptrain(request):
    return render(request, "gymsite/group_train.html")

def personaltrain(request):
    return render(request, "gymsite/personal_train.html")

def activities(request):
    return render(request, "gymsite/activities.html")

def aboutgym(request):
    return render(request, "gymsite/about_gym.html")

def trainers(request):
    return render(request, "gymsite/trainers.html")

def gavrylenko(request):
    return render(request, "gymsite/gavrylenko.html")

def mysan(request):
    return render(request, "gymsite/mysan.html")

def renivskiy(request):
    return render(request, "gymsite/renivskiy.html")

def shashkevych(request):
    return render(request, "gymsite/shashkevych.html")

def article(request):
    items = Articles.objects.all()
    context = {
        'items':items
    }
    return render(request, "gymsite/article.html", context)

def articleId(request, id):
    item = Articles.objects.get(id=id)
    context = {
        'item':item
    }
    return render(request, "gymsite/detail.html", context)

def abonement(request):
    items = Abonement.objects.all()
    exercise_abonements = Abonement.objects.filter(type='заняття')
    monthly_abonements = Abonement.objects.filter(type='місяці')
    context = {
        'items':items,
        'exercise_abonements': exercise_abonements,
        'monthly_abonements': monthly_abonements
    }
    return render(request, "gymsite/abonement.html", context)