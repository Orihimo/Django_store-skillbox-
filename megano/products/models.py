from django.db import models

from user_profile.models import Profile


class Sale(models.Model):
    salePrice = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    dateFrom = models.DateField()
    dateTo = models.DateField()


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/categories/", null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=128, verbose_name="Имя тега")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    fullDescription = models.TextField(null=False, blank=True)
    freeDelivery = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name="products")
    rating = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        upload_to="products/images/",
        default="products/images/default.png",
        verbose_name="Ссылка",
        null=True,
        blank=True,
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, related_name="reviews"
    )
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=255, null=True, blank=True)
    rate = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    # @property
    # def email(self):
    #     return self.author.email

    def __str__(self):
        return self.text


class Specification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="specifications",
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    value = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
