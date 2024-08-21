from typing import Tuple
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from .models import Producto, Categoria, Inventario, Registro_de_altas, Registro_de_bajas


# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    fields = ['nombre', 'abreviaciones', 'categoria', 'iba', 'unidad_medida']
    list_display = ('nombre', 'abreviaciones', 'categoria', 'mostrar_iba', 'codigo', 'codigo_barra',)
    list_display_links = ('nombre', 'abreviaciones')
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    list_display_links_limit = 2

    def mostrar_iba(self, obj):
        return f"{obj.iba}%"

    mostrar_iba.short_description = "IBA (%)"


admin.site.register(Producto, ProductoAdmin)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    list_display_links_limit = 1


admin.site.register(Categoria, CategoriaAdmin)


class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'mostrar_iba', 'mostrar_UM')
    list_display_links = ('producto', 'cantidad')
    list_filter = ('producto',)
    search_fields = ('producto__nombre',)
    list_display_links_limit = 2

    def mostrar_iba(self, obj):
        return f"{obj.producto.iba}%"

    mostrar_iba.short_description = "IBA (%)"

    def mostrar_UM(self, obj):
        return f"{obj.producto.unidad_medida}"

    mostrar_UM.short_description = "UM"


admin.site.register(Inventario, InventarioAdmin)


class Registro_de_altasAdmin(admin.ModelAdmin):
    fields = ['producto', 'cantidad', 'valor_unitario', 'fecha']
    list_display = ('producto', 'cantidad', 'get_iba_display', 'fecha', 'valor_unitario', 'importe_total')
    list_display_links = ('cantidad', 'producto')
    list_filter = ('producto', 'fecha')
    search_fields = ('producto__nombre',)
    list_display_links_limit = 2

    def get_iba_display(self, obj):
        return obj.producto.get_iba_display()

    get_iba_display.short_description = 'IBA'


admin.site.register(Registro_de_altas, Registro_de_altasAdmin)


class Registro_de_bajasAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha')
    list_display_links = ('cantidad', 'fecha')
    list_filter = ('producto', 'fecha')
    search_fields = ('producto__nombre',)
    list_display_links_limit = 2


admin.site.register(Registro_de_bajas, Registro_de_bajasAdmin)
