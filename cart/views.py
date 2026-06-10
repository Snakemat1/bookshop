from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from django.views.decorators.http import require_POST
from catalog.models import Book

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(book, quantity=quantity)
    return redirect("cart:detail")

@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect("cart:detail")




