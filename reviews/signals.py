from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Review

@receiver([post_delete, post_save], sender=Review)
def clear_book_reviews_cache(instance, sender, **kwargs):
    cache_key = f"book_reviews_{instance.book.id}"
    cache.delete(cache_key)

    