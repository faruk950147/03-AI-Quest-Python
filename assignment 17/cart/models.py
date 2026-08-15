# ===========================
# cart/models.py
# ===========================
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from store.models import Product, ProductVariant

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    paid = models.BooleanField(default=False)
    stored_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','product','variant','paid')
        ordering = ['id']
        verbose_name_plural = '01. Carts'

    @property
    def unit_price(self):
        if self.variant and self.variant.variant_price > Decimal('0.00'):
            return self.variant.variant_price
        return self.product.sale_price or Decimal('0.00')

    @property
    def subtotal(self):
        return (self.stored_unit_price * self.quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        if self.variant and self.variant.product != self.product:
            raise ValidationError("Variant does not belong to this product.")
        if self.variant and self.quantity > self.variant.available_stock:
            raise ValidationError(f"Only {self.variant.available_stock} unit(s) available.")
        elif not self.variant and self.quantity > self.product.available_stock:
            raise ValidationError(f"Only {self.product.available_stock} unit(s) available.")

    def save(self, *args, **kwargs):
        if not self.pk or Cart.objects.filter(pk=self.pk).values_list('variant_id', flat=True).first() != self.variant_id:
            self.stored_unit_price = self.unit_price
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        variant_str = f" - {self.variant}" if self.variant else ""
        return f"{self.user.username} - {self.product.title}{variant_str} ({self.quantity})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','product','variant')
        ordering = ['id']
        verbose_name_plural = '02. Wishlists'

    def __str__(self):
        variant_str = f" - {self.variant}" if self.variant else ""
        return f"{self.user.username} - {self.product.title}{variant_str}"
