from typing import Tuple

from django.contrib import admin
from .models import Producto, Categoria, Inventario, Registro_de_altas, Registro_de_bajas


# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviaciones', 'codigo', 'codigo_barra')
    list_display_links = ('nombre', 'abreviaciones')
    list_display_links_limit = 2


admin.site.register(Categoria)

admin.site.register(Inventario)


@admin.register(Registro_de_altas)
class Registro_de_altasAdmin(admin.ModelAdmin):
    list_display = ('cantidad', 'fecha')
    list_display_links = ('cantidad', 'fecha')
    list_display_links_limit = 2


@admin.register(Registro_de_bajas)
class Registro_de_bajasAdmin(admin.ModelAdmin):
    list_display = ('cantidad', 'fecha')
    list_display_links = ('cantidad', 'fecha')
    list_display_links_limit = 2
