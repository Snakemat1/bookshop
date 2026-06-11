from django.db import models
from django.conf import settings

class SavedCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_cart")
    data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
    
