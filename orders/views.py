from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order
from django.db import transaction
from django.core.exceptions import PermissionDenied

@login_required
def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form =  OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order = order,
                        book = item["book"],
                        price = item["price"],
                        quantity = item["quantity"],
                    )
                cart.clear()
                return redirect("orders:detail", pk = order.pk)
    else:
        form = OrderCreateForm(user=request.user)
    return render(request, "orders/order_create.html", {"form": form, "cart": cart})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user:
        raise PermissionDenied
    return render(request, "orders/order_detail.html", {"order": order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})