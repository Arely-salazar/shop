from django.contrib import admin
from .models import Categoria, Producto

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug':('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'precio', 'disponibilidad','existencias','created','updated']
    list_filter  = ['disponibilidad', 'created', 'updated']
    list_editable = ['precio', 'disponibilidad','existencias']
    prepopulated_fields = {'slug':('nombre',)}