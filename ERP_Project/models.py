import random
from datetime import date

from django.db import models
from django.db.models.signals import post_save
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from io import BytesIO
from django.dispatch import receiver



class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


# This is model of Products
class Producto(models.Model):
    TIPO_CHOICES = (
        (0, '0%'),
        (4, '4%'),
        (5, '5%'),
        (10, '10%'),
        (21, '21%')
    )
    TIPO_UNIDADES = (
        ('Gr', 'Gr'),
        ('Kg', 'Kg'),
        ('Ml', 'Ml'),
        ('Lt', 'Lt'),
        ('Cl', 'CL')
    )
    nombre = models.CharField(max_length=255)
    abreviaciones = models.CharField(max_length=10)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=255, null=True, blank=True)
    codigo_barra = models.ImageField(upload_to='codigos_barra', null=True, blank=True)
    codigo_barra_number = models.CharField(max_length=255, null=True, blank=True)
    iba = models.IntegerField(choices=TIPO_CHOICES)
    unidad_medida = models.CharField(choices=TIPO_UNIDADES, max_length=10)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Generar un número aleatorio entre 1 y 999
        random_number = random.randint(1, 999999999999)

        # Convertir el número aleatorio a una cadena de 12 dígitos con ceros a la izquierda
        self.codigo = f"{self.abreviaciones}-{random_number:012d}"

        try:
            # Generar el código de barras
            EAN = get_barcode_class('ean13')
            ean = EAN(str(random_number), writer=ImageWriter())
            self.codigo_barra_number = ean
            barcode_image = ean.render()

            # Guarda la imagen del código de barras en el campo
            image_io = BytesIO()
            barcode_image.save(image_io, format='PNG')
            self.codigo_barra.save(f"{self.codigo}.png", ContentFile(image_io.getvalue()), save=False)
        except (ValueError, RuntimeError) as e:
            # Si hay un error, dejar el campo codigo_barra como None
            self.codigo_barra = None
            print(f"Error generando código de barras: {e}")

        super().save(*args, **kwargs)


# This is model of inventary
class Inventario(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)



# This model is for taking the products who are deregistered from the warehouse
class Registro_de_bajas(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fecha = models.DateField()


class Registro_de_altas(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    valor_unitario = models.PositiveIntegerField(default=0)
    importe_total = models.PositiveIntegerField(default=0)
    fecha = models.DateField()

    def save(self, *args, **kwargs):
        self.importe_total = self.valor_unitario * self.cantidad + self.producto.iba

        super().save(*args, **kwargs)


# actualiza el inventario cuando se inserta un registro de altas
@receiver(post_save, sender=Registro_de_altas)
def actualizar_inventario_altas(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        cantidad = instance.cantidad

        # Buscar o crear el registro de inventario
        inventario, created = Inventario.objects.get_or_create(producto=producto, defaults={'cantidad': 0})
        inventario.cantidad += cantidad
        inventario.save()


# actualiza el inventario cuando se inserta un registro de bajas
@receiver(post_save, sender=Registro_de_bajas)
def actualizar_inventario_bajas(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        cantidad = instance.cantidad

        # Buscar o crear el registro de inventario
        inventario, created = Inventario.objects.get_or_create(producto=producto, defaults={'cantidad': 0})
        inventario.cantidad -= cantidad
        inventario.save()


@receiver(post_save, sender=Producto)
def crear_registro_inventario(sender, instance, created, **kwargs):
    if created:
        Inventario.objects.create(
            producto=instance,
            cantidad=0
        )