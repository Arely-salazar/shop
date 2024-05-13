from django.urls import path
from . import views

app_name ='shop'
urlpatterns=[
    path('', views.producto_lista, name='producto_lista'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('<slug:categoria_slug>/', views.producto_lista, name='producto_lista_by_categoria'),
    path('<int:id>/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
]