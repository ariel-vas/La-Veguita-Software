from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListCreate.as_view(), name="user-view-create-list"),
    path("users/<int:id>", views.UserRetrieveUpdateDestroy.as_view(), name="user-view-retrieve-update-destroy"),
    path("product/", views.ProductListCreate.as_view(), name="product-view-create-list"),
    path("product/<int:id_product>", views.ProductRetrieveUpdateDestroy.as_view(), name="product-view-retrieve-update-destroy"),
]