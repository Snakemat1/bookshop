from django.db import models
from django.conf import settings
from catalog.models import Book
from django.conf import settings

STATUS_PENDING  = 'pending'
STATUS_PAID     = 'paid'
STATUS_SHIPPED  = 'shipped'
STATUS_DONE     = 'done'
STATUS_CANCELED = 'canceled'

STATUS_CHOICES = [
    (STATUS_PENDING,  'Ожидает оплаты'),
    (STATUS_PAID,     'Оплачен'),
    (STATUS_SHIPPED,  'Отправлен'),
    (STATUS_DONE,     'Выполнен'),
    (STATUS_CANCELED, 'Отменён'),
]


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.price* self.quantity

