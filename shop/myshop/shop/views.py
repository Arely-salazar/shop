from django.shortcuts import render, get_object_or_404, redirect  
from .models import Categoria, Producto
from cart.forms import CartAddProductForm

# Create your views here.

def producto_lista(request, categoria_slug=None):
    categoria = None
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(disponibilidad=True)

    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        productos = productos.filter(categoria=categoria)
    return render(request, 
                  'shop/producto/lista.html',
                  {'categoria':categoria,
                   'categorias': categorias,
                   'productos': productos})

def producto_detalle(request, id, slug):
    producto = get_object_or_404(Producto, 
                                 id=id, 
                                 slug=slug, 
                                 disponibilidad=True)
    cart_product_form = CartAddProductForm()

    
    if request.method == 'POST':
        cart_product_form = CartAddProductForm(request.POST, producto=producto)
        if cart_product_form.is_valid():
            # Procesa el formulario y agrega el producto al carrito
            pass
    
    return render(request, 
                  'shop/producto/detalle.html',
                  {'producto':producto,
                   'cart_product_form': cart_product_form})

def buscar_productos(request):
    query = request.GET.get('q')
    resultados = None
    if query:
        resultados = Producto.objects.filter(nombre__icontains=query)
    return render(request, 'shop/producto/buscar_productos.html', {'resultados': resultados, 'query': query})

#http://127.0.0.1:800/