from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListCreate.as_view(), name="user-view-create-list"),
    path("users/<int:id>", views.UserRetrieveUpdateDestroy.as_view(), name="user-view-retrieve-update-destroy"),
    path("subcategory/", views.SubcategoryListCreate.as_view(), name="subcategory-view-create-list"),
    path("subcategory/<int:id>", views.SubcategoryRetrieveUpdateDestroy.as_view(), name="subcategory-view-retrieve-update-destroy")
]