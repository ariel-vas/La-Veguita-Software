from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    class RolTypes(models.TextChoices):
        ADMIN = 'admin'
        vendor = 'vendor'

    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.TextField()
    rol = models.CharField(max_length=6, choices=RolTypes.choices)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Evita rehashear si ya está hasheada
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)