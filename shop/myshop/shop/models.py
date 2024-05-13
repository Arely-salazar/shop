from django.db import models
from django.urls import reverse

# BD PARA LA CATEGORIA Y PRODUCTOS

# DEFINIENDO LA CATEGORIA DE LOS PRODUCTOS
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['nombre']
        indexes = [models.Index(fields=['nombre']),]
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('shop:producto_lista_by_categoria',
                        args=[self.slug])
# DEFINIENDO  LOS PRODUCTOS
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='Productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', blank=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    existencias = models.PositiveIntegerField(default=0)  # Campo para las existencias del producto
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        indexes = [models.Index(fields=['id', 'slug']),
                   models.Index(fields=['nombre']),
                   models.Index(fields=['-created']),
                   ]

    def __str__(self):
        return self.nombre 
    
    def get_absolute_url(self):
        return reverse('shop:producto_detalle',
                        args=[self.id, self.slug])
    
    @property
    def esta_agotado(self):
        return self.existencias <= 0 