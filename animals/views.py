from django.shortcuts import render, get_object_or_404
from .models import Animal
from .filters import AnimalFilter

def animal_list(request):
    animal_filter = AnimalFilter(request.GET, queryset=Animal.objects.all())
    return render(request, 'animals/animal_list.html', {'filter': animal_filter})

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'animals/animal_detail.html', {'animal': animal})

from django.shortcuts import redirect, get_object_or_404
from .models import Animal
from .cart import cart_summary

def add_to_cart(request, animal_id):
    cart = request.session.get('cart', {})
    cart[animal_id] = cart.get(animal_id, 0) + 1
    request.session['cart'] = cart
    return redirect('animal_list')

def remove_from_cart(request, animal_id):
    cart = request.session.get('cart', {})
    if animal_id in cart:
        del cart[animal_id]
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    context = cart_summary(request)
    return render(request, 'animals/cart_view.html', context)


import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
import decimal
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = decimal('0.00')
    for animal_id, quantity in cart.items():
        animal = Animal.objects.get(pk=animal_id)
        total += animal.price * quantity
        items.append({'animal': animal, 'quantity': quantity})
    if request.method == 'POST':
        try:
            amount = int(total * 100)  # valor em centavos
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Pagamento por animais',
                source=request.POST['stripeToken']
            )
            request.session['cart'] = {}
            return redirect('success')
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'animals/checkout.html', {'total': total, 'public_key': settings.STRIPE_TEST_PUBLIC_KEY})

@csrf_exempt
def success(request):
    return render(request, 'animals/success.html')
