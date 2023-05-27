from django.urls import path
from . import views

app_name = 'cart'

urlpatterns  = [
    path(
        'add_to_cart/',
        views.CartItemCreateView.as_view(),
        name='add_to_cart'
    ),
    path(
        'cart/',
        views.CartItemListView.as_view(),
        name='cart'
    ),
    path(
        'delete_from_cart/',
        views.cart_item_delete,
        name='delete_from_cart'
    )
]