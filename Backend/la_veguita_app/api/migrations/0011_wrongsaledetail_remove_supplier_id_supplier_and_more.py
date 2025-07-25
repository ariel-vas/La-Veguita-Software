# Generated by Django 5.2 on 2025-06-26 07:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_batch_quantity_alter_batch_starting_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='WrongSaleDetail',
            fields=[
                ('id_wrong_sale_detail', models.AutoField(primary_key=True, serialize=False)),
                ('receipt_number', models.DecimalField(decimal_places=0, max_digits=10, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='id_supplier',
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='receipt_number',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=10, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='cellphone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='supplier',
            name='city',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='commune',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='supplier',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='line',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='rut',
            field=models.CharField(default='', max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='telephone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
