from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse,\
get_object_or_404
from orders.models import Orden

# CREAR UNA INSTANCIA DE STRIPE
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

# CREAR EL PROCESO DE PAGO
def payment_process(request):
    # OBTENER EL ID DE ACUERDO A LA SESIÓN QUE SE HA GUARDADO
    orden_id = request.session.get('orden_id', None)
    # OBTENER LA ORDEN
    orden = get_object_or_404(Orden, id=orden_id)
    #
    if request.method == 'POST':
        #
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        #
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        
        # DATOS DE LA SESIÓN DE PAGO DE STRIPE
        session_data = {
        'mode': 'payment',
        'client_reference_id': orden.id,
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': []
        }

        # AÑADIR ELEMENTOS DEL PEDIDO A LA SESIÓN DE PAGO DE STRIPE
        for item in orden.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.precio * Decimal('100')),
                    'currency': 'mxn',
                    'product_data': {
                        'name': item.producto.nombre,
                    },
                },
                'quantity': item.cantidad,
            })

        # CREAR SESIÓN DE PAGO STRIPE
        session = stripe.checkout.Session.create(**session_data)

        # REDIRIGIR AL FORMULARIO DE PAGO DE STRIPE
        return redirect(session.url, code=303)
    
    else:
        return render(request, 'payment/process.html',locals())
    
def payment_completed(request):
    orden_id = request.session.get('orden_id')
    orden = Orden.objects.get(id=orden_id)
    return render(request, 'payment/completed.html', {'orden': orden})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')


