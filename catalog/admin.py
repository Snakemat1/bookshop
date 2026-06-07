from django.contrib import admin
from .models import Category, Author, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {"slug": ("name",)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name", "last_name")}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "price", "stock", "available"]
    list_filter = ["available", "category"]
    prepopulated_fields = {"slug": ("title",)}


