from django.urls import path
from gymsite.views import index, grouptrain, personaltrain, activities, aboutgym, trainers, gavrylenko
from gymsite.views import mysan, renivskiy, shashkevych, article, abonement, create_checkout_session, stripe_webhook, success, cancel

urlpatterns = [
    path('', index, name="index"),
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
    path('abonement', abonement, name='abonement'),
    path('create-checkout-session/<int:abonement_id>/', create_checkout_session, name='create-checkout-session'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]

