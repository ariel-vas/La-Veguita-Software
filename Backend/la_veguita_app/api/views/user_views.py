from django.shortcuts import render
from rest_framework import generics
from ..models import User
from ..serializers import UserSerializer

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.views import View
import json

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            user = User.objects.get(email=email)

            if check_password(password, user.password):
                request.session["user_id"] = user.id_user
                request.session["rol"] = user.rol
                return JsonResponse({"success": True, "rol": user.rol})
            else:
                return JsonResponse({"success": False, "message": "Contraseña incorrecta"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Usuario no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": "Error en el servidor"}, status=500)
    else:
        return JsonResponse({"message": "Método no permitido"}, status=405)
    
def logout_view(request):
    request.session.flush()
    return JsonResponse({"success": True, "message": "Sesión cerrada"})

def whoami_view(request):
    user_id = request.session.get("user_id")
    if user_id is None:
        return JsonResponse({"authenticated": False}, status=401)
    
    try:
        user = User.objects.get(id_user=user_id)
        return JsonResponse({
            "authenticated": True,
            "id": user.id_user,
            "username": user.username,
            "email": user.email,
            "rol": user.rol,
        })
    except User.DoesNotExist:
        return JsonResponse({"authenticated": False}, status=401)