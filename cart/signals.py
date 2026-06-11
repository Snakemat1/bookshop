from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from.models import SavedCart

@receiver(user_logged_out)
def save_cart_on_logout(sender, user, request, **kwargs):
    cart_data = request.session.get("cart", {})
    SavedCart.objects.update_or_create(user=user, defaults={"data": cart_data})
                                       
@receiver(user_logged_in)
def restore_cart_on_login(sender, user, request, **kwargs):
    try:
        saved = SavedCart.objects.get(user=user)
        request.session["cart"] = saved.data
        saved.delete()
    except SavedCart.DoesNotExist:
        pass
    