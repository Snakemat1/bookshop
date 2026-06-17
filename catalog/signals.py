from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category

@receiver([post_delete, post_save], sender=Category)
def clear_categories_cache(sender, **kwargs):
    cache.delete("categories_list")