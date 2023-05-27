from django.contrib.sessions.models import Session
from .models import Cart

def cart(request):
    """
    получение количества товара в корзине
    """
    session = Session.objects.get(session_key = request.session.session_key)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, session=session)
    else:
        cart, _ = Cart.objects.get_or_create(session=session)
    return {
        'cart_count':cart.count
    }