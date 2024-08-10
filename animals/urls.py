from django.urls import path
from . import views

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('add-to-cart/<int:animal_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:animal_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
]
