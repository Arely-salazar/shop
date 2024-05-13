from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Producto

# Create your models here.

class Orden(models.Model):
    primer_nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pagado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
        models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Orden {self.id}'  
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrdenProductos(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='orden_items', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad= models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.precio * self.cantidad