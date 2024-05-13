from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Producto
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    form = CartAddProductForm(request.POST)

    # Verificar la EXISTENCIA del producto antes de procesar el formulario
    if producto.existencias > 0:
        if form.is_valid():
            cd = form.cleaned_data
            # Restar la cantidad vendida del atributo existencias
            producto.existencias -= cd['quantity']
            producto.save()
            cart.add(producto=producto,
                    quantity=cd['quantity'],
                    override_quantity=cd['override'])
            return redirect('cart:cart_detalle')
    else:
        
        return redirect('shop:producto_detalle', producto.id, producto.slug)

   
@require_POST
def cart_remove(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
     # Agregar la cantidad removida al atributo existencias
    producto.existencias += cart.cart[str(producto.id)]['quantity']
    producto.save()
    cart.remove(producto)
    return redirect('cart:cart_detalle')


def cart_detalle(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
        # Verificar la disponibilidad del producto y establecer una bandera para la plantilla
        item['disponible'] = item['producto'].existencias > 0
    return render(request, 'cart/detalle.html', {'cart': cart})