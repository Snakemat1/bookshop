from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Author, Category
from django.db.models import Avg, Count
from reviews.forms import ReviewForm
from orders.models import OrderItem

class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"

class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        context["reviews"] = book.reviews.select_related("user")
        
        aggregates = book.reviews.aggregate(avg_rating=Avg("rating"), review_count=Count("id"))
        context["avg_rating"] = aggregates["avg_rating"]
        context["review_count"] = aggregates["review_count"]

        context["review_form"] = ReviewForm()
        
        if self.request.user.is_authenticated:
            user_review = book.reviews.filter(user=self.request.user).first()
            context["user_review"] = user_review
            has_purchased = OrderItem.objects.filter(order__user=self.request.user, book=book).exists()
            context["can_review"] = has_purchased and user_review is None
        else:
            context["user_review"] = None
            context["can_review"] = False
        return context

class AuthorListView(ListView):
    model = Author
    template_name = "catalog/author_list.html"
    context_object_name = "authors"

class AuthorDetailView(DetailView):
    model = Author
    template_name = "catalog/author_detail.html"
    context_object_name = "author"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["books"] = self.object.book_set.all()

        return context
    
class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"

class CategoryDetailView(DetailView):
    model = Category
    template_name = "catalog/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["books"] = self.object.books.all()

        return context
    
