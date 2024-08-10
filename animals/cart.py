from decimal import Decimal

def cart_summary(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    for animal_id, quantity in cart.items():
        animal = animal.objects.get(pk=animal_id)
        total += animal.price * quantity
        items.append({'animal': animal, 'quantity': quantity})
    return {'items': items, 'total': total}
