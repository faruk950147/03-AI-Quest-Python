from django.db import models
from store.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()
class Cart(models.Model):
    """
    Shopping cart item model for a user.
    Tracks product, quantity, and payment status.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']  # oldest cart items first
        verbose_name_plural = '01. Carts'

    @property
    def subtotal(self):
        """
        Calculate total price for this cart item.
        """
        return self.product.sale_price * self.quantity

    def __str__(self):
        """
        Human-readable representation for admin or debugging.
        """
        return f'{self.user.username} - {self.product.title} ({self.quantity})'
