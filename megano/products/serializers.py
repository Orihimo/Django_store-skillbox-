from rest_framework import serializers

from user_profile.models import Profile
from .models import Product, Category, Tag, Image, Review, Specification


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "fullName", "email")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id"]


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["name", "value"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["src", "alt"]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullName")
    email = serializers.CharField(source="author.email")

    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]

    def create(self, validated_data):
        return Review.objects.create(
            author=validated_data.get("author"),
            email=validated_data.get("email"),
            text=validated_data.get("text"),
            rate=validated_data.get("rate"),
            product_id=validated_data.get("product_id"),
        )


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = TagSerializer(many=True)
    images = ImageSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    salePrice = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "price",
            "salePrice",
            "dateFrom",
            "dateTo",
            "title",
            "images",
        )

    def get_reviews(self, obj):
        return obj.rel_name_products.count()

    def get_images(self, obj):
        return [{"src": image.src.url, "alt": image.alt} for image in obj.images.all()]

    def get_salePrice(self, obj):
        return obj.sale.salePrice

    def get_dateFrom(self, obj):
        return str(obj.sale.dateFrom)[5:]

    def get_dateTo(self, obj):
        return str(obj.sale.dateTo)[5:]


class PopularProductsSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_images(self, obj):
        return [{"src": image.src.url, "alt": image.alt} for image in obj.images.all()]

    def get_tags(self, obj):
        return [{"id": tag.id, "name": tag.name} for tag in obj.tags.all()]


class CategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "title", "image", "subcategories")

    def get_image(self, obj):
        return [{"src": image.src.url, "alt": image.alt} for image in obj.images.all()][
            0
        ]

    def get_subcategories(self, obj):
        return [
            {
                "id": obj.id,
                "title": obj.title,
                "image": [
                    {"src": image.src.url, "alt": image.alt}
                    for image in obj.images.all()
                ][0],
            }
        ]
