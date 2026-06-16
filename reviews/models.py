from django.db import models
from django.conf import settings
from catalog.models import Book
from django.core.validators import MinValueValidator, MaxValueValidator
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        error_messages={"min_value": "Оценка должна быть не меньше 0"},
        validators=[MinValueValidator(1, message="Оценка должна быть не меньше 1"), MaxValueValidator(5, message="Оценка должна быть не больше 5")])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "book"], name="unique_review_per_user_book")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} о '{self.book}' - {self.rating}/5"