from decimal import Decimal
from django.conf import settings
from shop.models import Producto

# CLASE PARA EL CARRITO
class Cart:
    # iniciar un carrito 
    def __init__(self, request):
       #iniciar el cart
       self.session = request.session
       cart = self.session.get(settings.CART_SESSION_ID)
       # SI NO HAY UNA CARRO CREADO
       if not cart:
           # guardar y vaciar el carro en la sesión
           cart = self.session[settings.CART_SESSION_ID] = {}
        # CREAR EL CARRO
       self.cart = cart

    #Función para agregar productos al carrito
    def add(self, producto, quantity=1, override_quantity=False):
        producto_id = str(producto.id)
        # SI EL PRODUCTO NO ESTA EN EL CARRO AGREGARLO
        if producto_id not in self.cart:
            self.cart[producto_id] = {'quantity': 0,
                                      'precio': str(producto.precio)}

        # ACTUALIZAR LA CANTIDAD DE PRODUCTOS
        if override_quantity:
            self.cart[producto_id]['quantity'] = quantity
        else:
            self.cart[producto_id]['quantity'] += quantity
        self.save()
    
    # GUARDAR 
    def save(self):
        self.session.modified = True

    # ELIMINAR PRODUCTOS DEL CARRITO
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
    
    # MOSTRAR LA CANTIDAD DE PRODUCTOS
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    # MOSTRAR EL TOTAL DE LOS PRODUCTOS
    def get_total_precio(self):
        return sum(Decimal(item['precio']) * item['quantity'] for item in self.cart.values())
    
    # LIMPIAR EL CARRITO
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save