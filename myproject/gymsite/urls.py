from django.urls import path
from gymsite.views import index, grouptrain, personaltrain, activities, aboutgym, trainers, gavrylenko
from gymsite.views import mysan, renivskiy, shashkevych, article, abonement

urlpatterns = [
    path('', index),
    path('grouptrain', grouptrain),
    path('personaltrain', personaltrain),
    path('activities', activities),
    path('aboutgym', aboutgym),
    path('trainers', trainers),
    path('gavrylenko', gavrylenko),
    path('mysan', mysan),
    path('renivskiy', renivskiy),
    path('shashkevych', shashkevych),
    path('article', article),
    path('abonement', abonement)
]

