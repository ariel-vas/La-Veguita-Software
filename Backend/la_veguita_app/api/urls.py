from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListCreate.as_view(), name="user-view-create-list"),
    path("users/<int:id>", views.UserRetrieveUpdateDestroy.as_view(), name="user-view-retrieve-update-destroy"),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/create', views.ProductCreateView.as_view(), name='product-create'),
    path("product/<int:id_product>", views.ProductRetrieveUpdateDestroy.as_view(), name="product-view-retrieve-update-destroy"),
    path("subcategory/", views.SubCategoryListCreate.as_view(), name="subcategory-view-create-list"),
    path("subcategory/<int:id>", views.SubCategoryRetrieveUpdateDestroy.as_view(), name="subcategory-view-retrieve-update-destroy"),
    path("category/", views.CategoryListCreate.as_view(), name="category-view-create-list"),
    path("category/<int:id>", views.CategoryRetrieveUpdateDestroy.as_view(), name="category-view-retrieve-update-destroy"),
    path("sales/", views.SaleListCreate.as_view(), name="sale-view-create-list"),
    path("sales/<int:id_sale>", views.SaleRetrieveUpdateDestroy.as_view(), name="sale-view-retrieve-update-destroy"),
    path("batch/", views.BatchListCreate.as_view(), name="batch-view-create-list"),
    path("batch/<int:id>", views.BatchRetrieveUpdateDestroy.as_view(), name="batch-view-retrieve-update-destroy"),
    path("sale_details/", views.SaleDetailListCreate.as_view(), name="sale_detail-view-create-list"),
    path("sale_details/<int:id_sale_detail>", views.SaleDetailRetrieveUpdateDestroy.as_view(), name="sale_detail-view-retrieve-update-destroy"),
    path("supplier/", views.SupplierListCreate.as_view(), name="supplier-view-create-list"),
    path("supplier/<int:id>", views.SupplierRetrieveUpdateDestroy.as_view(), name="supplier-view-retrieve-update-destroy")
]