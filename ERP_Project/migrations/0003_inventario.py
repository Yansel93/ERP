# Generated by Django 5.0.7 on 2024-08-01 03:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Project', '0002_producto_rename_products_categoria_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_produtos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ERP_Project.producto')),
            ],
        ),
    ]
