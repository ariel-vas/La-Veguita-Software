from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListCreate.as_view(), name="user-create-list"),
    path("users/<int:id_user>", views.UserRetrieveUpdateDestroy.as_view(), name="user-retrieve-update-destroy"),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/create', views.ProductCreateView.as_view(), name='product-create'),
    path("products/<int:id_product>", views.ProductRetrieveUpdateDestroy.as_view(), name="product-retrieve-update-destroy"),
    path("subcategories/", views.SubCategoryListCreate.as_view(), name="subcategory-create-list"),
    path("subcategories/<int:id_subcategory>", views.SubCategoryRetrieveUpdateDestroy.as_view(), name="subcategory-retrieve-update-destroy"),
    path('subcategories/<int:id_subcategory>/products/', views.ProductsBySubCategory.as_view(), name='products-by-subcategory'),
    path("categories/", views.CategoryListCreate.as_view(), name="category-create-list"),
    path("categories/<int:id_category>", views.CategoryRetrieveUpdateDestroy.as_view(), name="category-retrieve-update-destroy"),
    path('categories/<int:id_category>/products/', views.ProductsByCategory.as_view(), name='products-by-category'),
    path("sales/", views.SaleListCreate.as_view(), name="sale-create-list"),
    path("sales/<int:id_sale>", views.SaleRetrieveUpdateDestroy.as_view(), name="sale-retrieve-update-destroy"),
    path("batches/", views.BatchListCreate.as_view(), name="batch-create-list"),
    path("batches/<int:id_batch>", views.BatchRetrieveUpdateDestroy.as_view(), name="batch-retrieve-update-destroy"),
    path("sale_details/", views.SaleDetailListCreate.as_view(), name="sale_detail-create-list"),
    path("sale_details/<int:id_sale_detail>", views.SaleDetailRetrieveUpdateDestroy.as_view(), name="sale_detail-retrieve-update-destroy"),
    path("suppliers/", views.SupplierListCreate.as_view(), name="supplier-create-list"),
    path("suppliers/<int:id_supplier>", views.SupplierRetrieveUpdateDestroy.as_view(), name="supplier-retrieve-update-destroy")
]