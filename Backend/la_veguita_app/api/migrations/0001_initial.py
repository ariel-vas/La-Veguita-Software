# Generated by Django 5.2 on 2025-05-08 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('rol', models.CharField(choices=[('admin', 'Admin'), ('vendor', 'Vendor')], max_length=6)),
            ],
        ),
    ]
