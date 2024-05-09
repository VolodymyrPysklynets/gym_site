import stripe
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Articles, Abonement, Purchase
from django.contrib.auth.models import User

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

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        abonement_id = session.get('metadata', {}).get('abonement_id')
        customer_email = session.get('customer_email')

        if abonement_id and customer_email:
            try:
                abonement = Abonement.objects.get(id=abonement_id)
                Purchase.objects.create(email=customer_email, abonement=abonement)
            except Abonement.DoesNotExist:
                return HttpResponse(status=404)
        return HttpResponse(status=200)
    return HttpResponse(status=200)

def create_checkout_session(request, abonement_id):
    abonement = Abonement.objects.get(id=abonement_id)
    try:
        print("Creating Stripe session with metadata:", {'abonement_id': str(abonement_id)})
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'uah',
                        'product_data': {
                            'name': abonement.name,
                        },
                        'unit_amount': abonement.price * 100,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_email=request.POST.get('email'),
            metadata={'abonement_id': str(abonement_id)},
            success_url=request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('cancel')),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            abonement_id = session.metadata.get('abonement_id') 
            if abonement_id:
                abonement = Abonement.objects.get(id=abonement_id)
                return render(request, "gymsite/success.html", {"abonement": abonement})
            else:
                return HttpResponse('abonement_id не знайдено в метаданих', status=400)
        except stripe.error.StripeError as e:
            return HttpResponse(str(e), status=400)
        except Abonement.DoesNotExist:
            return HttpResponse('Абонемент не знайдений', status=404)
    else:
        return HttpResponse('session_id не передано', status=400)

def cancel(request):
    return render(request, "gymsite/cancel.html", {
        "message": "Ваш платіж було скасовано. Ви можете спробувати знову."
    })