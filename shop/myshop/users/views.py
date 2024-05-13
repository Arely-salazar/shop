from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Create your views here.

class Registro(View):
    #muestra el formulario
    def get(self, request):
        form = UserCreationForm()
        return render(request, "registro/registro.html", {"form": form})

    #envio la información del formulario
    def post(self, request):
         form = UserCreationForm(request.POST)
         # VERIFICAR SI ES VALIDO LOS DATOS INTRODUCIDOS
         if form.is_valid():
            #guardar los datos del formulario en la variable usuario
            usuario = form.save(commit=False)
            primer_nombre = request.POST.get('primer_nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('correo')
            # Asignar los datos de órdenes al usuario
            usuario.first_name = primer_nombre
            usuario.last_name = apellido  # Asignar el apellido al campo last_name
            usuario.email = correo
            usuario.save()

            #login automatico
            login(request, usuario)
            #rediccionar a la página de inicio
            return redirect('shop:producto_lista')
         else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "registro/registro.html", {"form": form})

#FUNCIÓN PARA CERRAR SESIÓN        
def cerrar_sesion(request):
    logout(request)
    return redirect("shop:producto_lista")

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            #verificar con la bd
            usuario = authenticate(username = nombre_usuario, password = password)
            #SI ENCUENTRA AL USUARIO LO MANDA A LA PÁGINA PRINCIPAL
            if usuario is not None:
                login(request, usuario)
                return redirect("shop:producto_lista")
            #SI NO LO ENCUENTRA AL USUARIO MOSTRAR
            else:
                messages.error(request, "usuario no encontrado")
        else:
            messages.error(request, "información incorrecta")
            
    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})
