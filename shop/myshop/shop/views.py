from django.shortcuts import render, get_object_or_404  
from .models import Categoria, Producto

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
    
    return render(request, 
                  'shop/producto/detalle.html',
                  {'producto':producto})

#http://127.0.0.1:800/