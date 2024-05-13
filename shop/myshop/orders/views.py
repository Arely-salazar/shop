from django.shortcuts import render, redirect
from .models import OrdenProductos
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import Orden

# CREAR ORDEN
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            if 'tarjeta' in request.POST:
                orden.pagado = True
            orden.save()
            for item in cart:
                OrdenProductos.objects.create(orden=orden, producto=item['producto'], precio=item['precio'],cantidad=item['quantity'])
            cart.clear()
            request.session['orden_id'] = orden.id
            if 'efectivo' in request.POST:
                return redirect('order:order_created')
            elif 'tarjeta' in request.POST:
                return redirect('payment:process')
    else:
        # Obtener información del usuario actual para prellenar el formulario
        if request.user.is_authenticated:
            usuario = request.user
            initial_data = {
                'primer_nombre': usuario.first_name,
                'apellido': usuario.last_name,
                'correo': usuario.email
            }
            form = OrderCreateForm(initial=initial_data)
        else:
            form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

def order_created(request):
    orden_id = request.session.get('orden_id')
    orden = Orden.objects.get(id=orden_id)
    return render(request, 'orders/order/created.html', {'orden': orden})
