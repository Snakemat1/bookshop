from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Review
from orders.models import OrderItem
from catalog.models import Book
from .forms import ReviewForm
from orders.models import STATUS_DONE

@login_required
def add_review(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    already_review = Review.objects.filter(user=request.user, book=book).exists()
    has_purchased = OrderItem.objects.filter(order__user=request.user, book=book, order__status = STATUS_DONE).exists()

    if already_review or not has_purchased:
        return redirect("catalog:book_detail", slug=book_slug)

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.save()
        return redirect("catalog:book_detail", slug=book_slug)

    # форма невалидна — рендерим book_detail.html с ошибками, без редиректа
    aggregates = book.reviews.aggregate(avg_rating=Avg("rating"), review_count=Count("id"))
    context = {
        "book": book,
        "reviews": book.reviews.select_related("user"),
        "avg_rating": aggregates["avg_rating"],
        "review_count": aggregates["review_count"],
        "review_form": form,  # форма с ошибками, не пустая ReviewForm()
        "user_review": None,
        "can_review": True,
    }
    return render(request, "catalog/book_detail.html", context)
