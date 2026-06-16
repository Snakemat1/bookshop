from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Author, Category
from django.db.models import Avg, Count
from reviews.forms import ReviewForm
from orders.models import OrderItem
from django.db.models import Q
from orders.models import STATUS_DONE
from .services import get_categories

class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset =  super().get_queryset().select_related("category").prefetch_related("authors")
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(authors__first_name__icontains=q) |
                Q(authors__last_name__icontains=q)
            )

        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        min_price = self.request.GET.get("min_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.GET.get("max_price")
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["categories"] = get_categories()
        return context
    
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
            has_purchased = OrderItem.objects.filter(order__user=self.request.user, book=book, order__status=STATUS_DONE,).exists()
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
    
