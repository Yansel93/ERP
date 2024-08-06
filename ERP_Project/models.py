import random
from django.db import models
from barcode import get_barcode_class
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from io import BytesIO


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


# This is model of Products
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    abreviaciones = models.CharField(max_length=10)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=255, null=True, blank=True)
    codigo_barra = models.ImageField(upload_to='codigos_barra', null=True, blank=True)

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
    cantidad = models.IntegerField()


# This model is for taking the products that arrive at the warehouse
class Registro_de_altas(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()


# This model is for taking the products who are deregistered from the warehouse
class Registro_de_bajas(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
