# Generated by Django 5.0.7 on 2024-08-06 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Project', '0011_rename_produto_registro_de_altas_producto_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventario',
            old_name='produto',
            new_name='producto',
        ),
    ]
