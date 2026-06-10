from django.urls import path
from .views import cart_detail, cart_add, cart_remove

app_name = "cart"

urlpatterns = [
    path("", cart_detail, name="detail"),
    path("add/<book_id>/", cart_add, name="add"),
    path("remove/<book_id>/", cart_remove, name="remove"),

]
