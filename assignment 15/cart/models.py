from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from store.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01. Carts'

    @property
    def subtotal(self):
        return round(self.product.sale_price * self.quantity, 2)

    def clean(self):
        if self.quantity > self.product.available_stock:
            raise ValidationError(f"Cannot add more than {self.product.available_stock} units of {self.product.title}.")

    def __str__(self):
        return f'{self.user.username} - {self.product.title} ({self.quantity})'
