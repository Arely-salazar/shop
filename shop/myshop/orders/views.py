from django.shortcuts import render
from .models import OrdenProductos
from .forms import OrderCreateForm
from cart.cart import Cart


# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            orden = form.save()
            for item in cart:
                OrdenProductos.objects.create(orden=orden, producto=item['producto'], precio=item['precio'],cantidad=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request, 
                          'orders/order/created.html',
                          {'order': orden})
    else:
        form = OrderCreateForm()
    return render(request, 
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
