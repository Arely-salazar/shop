from django.contrib import admin
from .models import Orden, OrdenProductos

class OrderItemInline(admin.TabularInline):
    model = OrdenProductos
    raw_id_fields = ['producto']

@admin.register(Orden)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'primer_nombre', 'apellido', 'correo',
    'direccion', 'codigo_postal', 'ciudad', 'pagado',
    'created', 'updated']
    list_filter = ['pagado', 'created', 'updated']
    inlines = [OrderItemInline]

# Register your models here.
