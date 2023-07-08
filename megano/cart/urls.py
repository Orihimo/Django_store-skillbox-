from django.urls import path
from .views import CartDetailView

app_name = "cart"


urlpatterns = [
    path("basket", CartDetailView.as_view(), name="basket"),
]
