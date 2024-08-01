from typing import Tuple

from django.contrib import admin
from .models import Producto, Categoria, Inventario


# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviaciones', 'codigo', 'codigo_barra')
    list_display_links = ('nombre', 'abreviaciones')
    list_display_links_limit = 2


admin.site.register(Categoria)


admin.site.register(Inventario)

