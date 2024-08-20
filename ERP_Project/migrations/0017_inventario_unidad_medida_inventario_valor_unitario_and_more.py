# Generated by Django 5.0.7 on 2024-08-16 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERP_Project', '0016_alter_registro_de_altas_cantidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='unidad_medida',
            field=models.CharField(choices=[('Gr', 'Gr'), ('Kg', 'Kg'), ('Ml', 'Ml'), ('Lt', 'Lt'), ('Cl', 'CL')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventario',
            name='valor_unitario',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='cantidad',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
