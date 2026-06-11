from django.urls import path
from .views import order_create, order_detail, order_list

app_name = "orders"

urlpatterns = [
    path("", order_list, name="list"),
    path("create/", order_create, name="create"),
    path("<int:pk>/", order_detail, name="detail")
]
