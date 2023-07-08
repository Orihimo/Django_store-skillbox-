import math
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from rest_framework import status, request
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from user_profile.models import Profile
from .models import Product, Review, Tag, Category
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    SaleSerializer,
    PopularProductsSerializer,
    CategoryListSerializer,
)


class ProductAPIView(APIView):
    def get(self, request, id) -> Response:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ReviewCreateAPIView(APIView):
    def post(self, request, id):
        text_data = request.data["text"]
        rate_data = request.data["rate"]

        profile = Profile.objects.get(user=request.user.id)
        product = Product.objects.get(id=id)

        new_review = Review.objects.create(
            product=product,
            author=profile,
            text=text_data,
            rate=rate_data,
        )
        new_review.save()
        return Response(status=status.HTTP_201_CREATED)


class TagView(APIView):
    def get(self, request):
        tags = Tag.objects.all().values("id", "name")
        return Response(tags)


class SaleView(APIView):
    def get(self, request):
        products = Product.objects.all()

        return Response(
            {
                "items": [
                    SaleSerializer(product).data
                    for product in products
                    if product.sale is not None
                ],
                "currentPage": 3,
                "lastPage": 7,
            }
        )


class PopularProductsVIew(APIView):
    def get(self, request):
        products = Product.objects.all()
        return Response(
            [PopularProductsSerializer(product).data for product in products]
        )


class LimitedProductsView(APIView):
    """
    Для отображения используем PopularProductsSerializer, т.к. формат вывода данных аналогичный
    """

    def get(self, request):
        products = Product.objects.all()
        return Response(
            [PopularProductsSerializer(product).data for product in products]
        )


class BannersProductsView(APIView):
    """
    Для отображения используем PopularProductsSerializer, т.к. формат вывода данных аналогичный
    """

    def get(self, request):
        products = Product.objects.all()
        return Response(
            [PopularProductsSerializer(product).data for product in products]
        )


class CategoryAPIView(APIView):
    def get(self, request):
        produtcs = Product.objects.all()

        return Response([CategoryListSerializer(product).data for product in produtcs])


class CatalogListView(APIView):
    def get(self, request):
        # Получение параметров фильтрации из запроса
        min_price = request.GET.get("filter[minPrice]")
        max_price = request.GET.get("filter[maxPrice]")
        name = request.GET.get("filter[name]")
        available = request.GET.get("filter[available]")
        free_delivery = request.GET.get("filter[freeDelivery]")

        # Получение параметров сортировки из запроса
        sort = request.GET.get("sort")
        sort_type = request.GET.get("sortType")

        # Получение параметров постраничного вывода из запроса
        current_page = int(request.GET.get("currentPage", 1))
        items_per_page = int(request.GET.get("itemsPerPage", 20))

        # Фильтрация товаров
        products = Product.objects.all()
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if name:
            products = products.filter(title__icontains=name)
        if available == "true":
            products = products.filter(count__gt=0)
        if free_delivery == "true":
            products = products.filter(freeDelivery=True)

        # Сортировка товаров
        if sort == "rating":
            if sort_type == "dec":
                products = products.order_by("-rating")
            else:
                products = products.order_by("rating")
        elif sort == "price":
            if sort_type == "dec":
                products = products.order_by("-price")
            else:
                products = products.order_by("price")
        elif sort == "reviews":
            if sort_type == "dec":
                products = products.annotate(reviews_count=Count("reviews")).order_by(
                    "-reviews_count"
                )
            else:
                products = products.annotate(reviews_count=Count("reviews")).order_by(
                    "reviews_count"
                )
        elif sort == "date":
            if sort_type == "dec":
                products = products.order_by("-date")
            else:
                products = products.order_by("date")

        # Постраничный вывод товаров
        total_items = products.count()
        total_pages = math.ceil(total_items / items_per_page)
        start_index = (current_page - 1) * items_per_page
        end_index = start_index + items_per_page
        products = products[start_index:end_index]

        # Сериализация товаров
        serializer = PopularProductsSerializer(products, many=True)

        # Формирование ответа
        response_data = {
            "items": serializer.data,
            "currentPage": current_page,
            "lastPage": total_pages,
        }
        return Response(response_data)
