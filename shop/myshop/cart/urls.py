from django.urls import path
from . import views

app_name ='cart'
urlpatterns=[
    path('', views.cart_detalle, name='cart_detalle'),
    path('add/<int:producto_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:producto_id>/', views.cart_remove, name='cart_remove'),
]