import json
from typing import Any
from django.db.models.query import QuerySet

from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.views.generic.list import ListView

from cart.models import Cart, CartItem
from main.models import Product


class CartItemCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        """
        добавление товара в корзину
        """
        data = json.loads(request.body)
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            try:
                session = Session.objects.get(session_key=request.session.session_key)
                cart, _ = Cart.objects.get_or_create(session=session)
            except Session.DoesNotExist:
                data = {
                    'success': False
                }
                return JsonResponse(data=data, status=500)
        try:
            product = Product.objects.get(id=data.get('id'))
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                count=data.get('count', 1)
            )
            data = {
                'success': True,
                'count': cart.count
            }
            return JsonResponse(data=data, status=201)
        except Product.DoesNotExist:
            data = {
                'success': False
            }
            return JsonResponse(data=data, status=500)


class CartItemListView(ListView):
    model = CartItem
    template_name = 'cart/cart_item/list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        user = self.request.user
        empty = CartItem.objects.none()
        if user.is_authenticated:
            try:
                cart = Cart.objects.get(user=user)
                return cart.items.all()
            except Cart.DoesNotExist:
                return empty
        else:
            try:
                session = Session.objects\
                .get(session_key=self.request.session.session_key)
                return Cart.objects.get(session=session).items.all()
            except (Cart.DoesNotExist, Session.DoesNotExist):
                return empty


def cart_item_delete(request):
    """
    удаление товара из корзины
    """
    try:
        data = json.loads(request.body)
        cart_item = CartItem.objects.get(id=data.get('id'))
        cart = cart_item.cart
        cart_item.delete()
        data = {
            'success': True,
            'count': cart.items.count()
        }
        return JsonResponse(data=data, status=202)
    except CartItem.DoesNotExist:
        data = {
            'success': True
        }
        return JsonResponse(data=data, status=202)
    except KeyError:
        data = {
            'success': False
        }
        return JsonResponse(data=data, status=500)
