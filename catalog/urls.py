from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("books/<slug:slug>/", views.BookDetailView.as_view(), name="book_detail"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("authors/", views.AuthorListView.as_view(), name="author_list"),
    path("authors/<slug:slug>/", views.AuthorDetailView.as_view(), name="author_detail")
]
