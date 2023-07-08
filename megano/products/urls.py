from django.urls import path
from .views import (
    ProductAPIView,
    ReviewCreateAPIView,
    TagView,
    SaleView,
    PopularProductsVIew,
    LimitedProductsView,
    BannersProductsView,
    CategoryAPIView,
    CatalogListView,
)

app_name = "products"


urlpatterns = [
    path("product/<int:id>/", ProductAPIView.as_view(), name="product-detail"),
    path("product/<int:id>/reviews", ReviewCreateAPIView.as_view(), name="add_review"),
    path("tags/", TagView.as_view(), name="tag"),
    path("sales/", SaleView.as_view(), name="sale"),
    path("products/popular/", PopularProductsVIew.as_view(), name="products_popular"),
    path("products/limited/", LimitedProductsView.as_view(), name="products_limited"),
    path("banners/", BannersProductsView.as_view(), name="banners"),
    path("categories/", CategoryAPIView.as_view(), name="category-list"),
    path("catalog/", CatalogListView.as_view(), name="catalog"),
]
