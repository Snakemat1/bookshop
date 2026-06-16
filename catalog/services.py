from .models import Category
from django.core.cache import cache

def get_categories():
    return cache.get_or_set("categories_list", lambda: list(Category.objects.all()), timeout=3600)