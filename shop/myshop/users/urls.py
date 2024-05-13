from django.urls import path
from .views import Registro, cerrar_sesion, iniciar_sesion

app_name = 'users'

urlpatterns = [
    path('', Registro.as_view(), name='Usuarios'),
    path('cerrrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('iniciar_sesion', iniciar_sesion, name='iniciar_sesion'),
]
