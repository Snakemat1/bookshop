from django.core.cache import cache
from django.db.models import Avg, Count

def get_book_reviews_data(book):
    cache_key = f"book_reviews_{book.id}"
    return cache.get_or_set(
        cache_key,
        lambda: {
            "reviews": list(book.reviews.select_related("user")),
            **book.reviews.aggregate(avg_rating=Avg("rating"), review_count=Count("id")),
        },
        timeout=600,
    )