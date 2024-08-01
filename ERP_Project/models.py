import random
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


# This is model of Products
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    abreviaciones = models.CharField(max_length=10)
    codigo = models.CharField(max_length=255)
    codigo_barra = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Generar un número aleatorio entre 1 y 999
        random_number = random.randint(1, 999)

        # Concatenar el código existente con el número aleatorio
        self.codigo = f"{self.abreviaciones}-{random_number:03d}"

        super().save(*args, **kwargs)


# This is model of inventary
class Inventario(models.Model):
    produto = models.ForeignKey(Producto, null=True, on_delete=models.CASCADE)
    alta = models.IntegerField()
    baja = models.IntegerField()




