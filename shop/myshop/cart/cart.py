from decimal import Decimal
from django.conf import settings
from shop.models import Producto


class Cart:
    # iniciar un carrito 
    def __init__(self, request):
       #iniciar el cart
       self.session = request.session
       cart = self.session.get(settings.CART_SESSION_ID)
       if not cart:
           # guardar y vaciar el carro en la sesión
           cart = self.session[settings.CART_SESSION_ID] = {}
       self.cart = cart

    #Función para agregar productos al carrito
    def add(self, producto, quantity=1, override_quantity=False):
        producto_id = str(producto.id)
        
        if producto_id not in self.cart:
            self.cart[producto_id] = {'quantity': 0,
                                      'precio': str(producto.precio)}
        if override_quantity:
            self.cart[producto_id]['quantity'] = quantity
        else:
            self.cart[producto_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()
    
    def __iter__(self):
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        cart = self.cart.copy()

        for producto in productos:
            cart[str(producto.id)]['producto'] = producto
        for item in cart.values():
            item['precio'] = Decimal(item['precio'])
            item['total_precio'] = item['precio'] * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_precio(self):
        return sum(Decimal(item['precio']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save