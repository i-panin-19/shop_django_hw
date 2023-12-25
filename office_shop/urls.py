from django.urls import path

from office_shop.apps import OfficeShopConfig
from office_shop.views import CategoryListView, ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, IndexView

app_name = OfficeShopConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/<int:pk>/', ProductListView.as_view(), name='products'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
