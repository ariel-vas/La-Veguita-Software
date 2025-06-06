# Generated by Django 5.2 on 2025-05-15 05:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_product_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock_unit',
            new_name='entry_stock_unit',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='id_user',
        ),
        migrations.AddField(
            model_name='product',
            name='exit_stock_unit',
            field=models.CharField(choices=[('unit', 'Unit'), ('kilo', 'Kilo')], default='unit', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='batch',
            name='entry_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='batch',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='critical_stock',
            field=models.DecimalField(decimal_places=4, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price_kilo',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price_unit',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.DecimalField(decimal_places=4, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale_quantity',
            field=models.DecimalField(decimal_places=4, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='saledetail',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='saledetail',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='saledetail',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddConstraint(
            model_name='saledetail',
            constraint=models.UniqueConstraint(fields=('sale', 'product'), name='unique_sale_product'),
        ),
    ]
