from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from store.models import Product, VariantOption

User = get_user_model()

# ======================== BASE MIXIN ========================
class BaseMixin(models.Model):
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        abstract = True

# ======================== CART MODEL ========================
class Cart(BaseMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(VariantOption, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    paid = models.BooleanField(_('paid'), default=False)
    stored_unit_price = models.DecimalField(_('stored_unit_price'), max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('user','product','variant','paid')
        ordering = ['id']
        verbose_name_plural = '01. Carts'
        
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["product"]),
            models.Index(fields=["variant"]),
            models.Index(fields=["paid"]),
        ]

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
        
        if self.variant and self.quantity > self.variant.stock:
            raise ValidationError(f"Only {self.variant.stock} unit(s) available.")
        
        elif not self.variant and self.quantity > self.product.stock:
            raise ValidationError(f"Only {self.product.stock} unit(s) available.")

    def save(self, *args, **kwargs):
        if not self.pk or Cart.objects.filter(pk=self.pk).values_list('variant_id', flat=True).first() != self.variant_id:
            self.stored_unit_price = self.unit_price
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        variant_str = f" - {self.variant}" if self.variant else ""
        return f"{self.user.username} - {self.product.title}{variant_str} ({self.quantity})"

# ======================== WISHLIST MODEL ========================
class Wishlist(BaseMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(VariantOption, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        unique_together = ('user','product','variant')
        ordering = ['id']
        verbose_name_plural = '02. Wishlists'
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["product"]),
            models.Index(fields=["variant"]),
        ]

    def __str__(self):
        variant_str = f" - {self.variant}" if self.variant else ""
        return f"{self.user.username} - {self.product.title}{variant_str}"
