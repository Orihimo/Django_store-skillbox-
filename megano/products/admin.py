from django.contrib import admin
from .models import Category, Tag, Product, Image, Review, Specification, Sale

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Specification)
admin.site.register(Sale)
