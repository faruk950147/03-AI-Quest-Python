from decimal import Decimal, ROUND_HALF_UP
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.db.models import F, Model, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Product, VariantOption

User = get_user_model()
SHIPPING_COST = Decimal('150.00')

# =============================
# Shipping Model
# =============================
class Shipping(models.Model):
    SHIPPING_CHOICES = (('Home', 'Home'), ('Office', 'Office'))
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shipping'
    )
    shipping_choice = models.CharField(_("shipping_choice"), max_length=20, choices=SHIPPING_CHOICES, default='Home')
    name = models.CharField(_("name"), max_length=150)
    country = models.CharField(_("country"), max_length=150)
    city = models.CharField(_("city"), max_length=150)
    home_city = models.CharField(_("home_city"), max_length=150)
    zip_code = models.CharField(_("zip_code"), max_length=15)
    phone = models.CharField(_("phone"), max_length=16)
    address = models.TextField(_("address"), max_length=500)

    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "01. Shipping"

    def __str__(self):
        return f"{self.user.username} Shipping"


# =============================
# Coupon Model
# =============================
class Coupon(models.Model):
    code = models.CharField(_('code'), max_length=50, unique=True)
    discount_percent = models.DecimalField(
        _('discount_percent'),
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('90.00'))],
        default=Decimal('0.00')
    )
    max_usage = models.PositiveIntegerField(_('max_usage'), default=1)
    used_count = models.PositiveIntegerField(_('used_count'), default=0)
    max_discount_amount = models.DecimalField(_('max_discount_amount'), max_digits=10, decimal_places=2, default=Decimal('1000.00'))
    active = models.BooleanField(_('active'), default=True)
    start_date = models.DateTimeField(_('start_date'), null=True, blank=True)
    end_date = models.DateTimeField(_('end_date'), null=True, blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "02. Coupon"
        indexes = [models.Index(fields=['code'])]
        constraints = [
            models.CheckConstraint(check=models.Q(discount_percent__lte=90), name='discount_percent_max_90')
        ]

    def is_valid(self, user=None):
        now = timezone.now()
        if not self.active:
            return False, "Coupon inactive"
        if self.start_date and now < self.start_date:
            return False, "Coupon not started"
        if self.end_date and now > self.end_date:
            return False, "Coupon expired"
        if self.used_count >= self.max_usage:
            return False, "Coupon usage limit reached"
        if user and Checkout.objects.filter(
            user=user,
            coupon=self,
            status__in=['accepted','packed','on_the_way','delivered']
        ).exists():
            return False, "You already used this coupon"
        return True, "Valid"

    def calculate_discount(self, subtotal: Decimal):
        discount = (subtotal * self.discount_percent / Decimal('100')).quantize(Decimal('0.01'), ROUND_HALF_UP)
        return min(discount, self.max_discount_amount)

    def __str__(self):
        return f"Coupon #{self.pk} - {self.code}"


# =============================
# Checkout Model
# =============================
class Checkout(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('packed','Packed'),
        ('on_the_way','On The Way'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
        ('refunded','Refunded')
    )
    PAYMENT_METHOD_CHOICES = (
        ('cod','Cash on Delivery'),
        ('paypal','PayPal'),
        ('card','Card')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(_('payment_method'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    is_finalized = models.BooleanField(_('is_finalized'), default=False)
    paid_at = models.DateTimeField(_('paid_at'), null=True, blank=True)
    total_amount = models.DecimalField(_('total_amount'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(_('discount_amount'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_amount = models.DecimalField(_('final_amount'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "03. Checkout"
        indexes = [models.Index(fields=['user','status'])]

    # ===============================
    # Calculate totals
    # ===============================
    def calculate_totals(self):
        subtotal = self.items.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
        subtotal = subtotal.quantize(Decimal('0.01'), ROUND_HALF_UP)
        discount = self.coupon.calculate_discount(subtotal) if self.coupon else Decimal('0.00')
        shipping = SHIPPING_COST
        final_total = max((subtotal - discount) + shipping, Decimal('0.00')).quantize(Decimal('0.01'), ROUND_HALF_UP)
        return subtotal, discount, final_total

    # ===============================
    # Finalize checkout safely
    # ===============================
    def finalization_checkout(self):
        with transaction.atomic():
            checkout = Checkout.objects.select_for_update().get(pk=self.pk)

            if checkout.is_finalized:
                raise ValidationError("Checkout already finalized")
            if not checkout.items.exists():
                raise ValidationError("No items in checkout")

            subtotal, discount, final_total = checkout.calculate_totals()

            # --- Validate coupon first ---
            if checkout.coupon:
                coupon = Coupon.objects.select_for_update().get(pk=checkout.coupon.pk)
                valid, msg = coupon.is_valid(user=checkout.user)
                if not valid:
                    raise ValidationError(msg)
                updated_coupon = Coupon.objects.filter(
                    pk=coupon.pk,
                    used_count__lt=F('max_usage')
                ).update(used_count=F('used_count') + 1)
                if not updated_coupon:
                    raise ValidationError("Coupon usage limit reached")

            # --- Deduct stock ---
            items = checkout.items.select_related('product','variant').select_for_update()
            for item in items:
                if item.variant:
                    updated_stock = VariantOption.objects.filter(
                        pk=item.variant.pk,
                        stock__gte=item.quantity
                    ).update(stock=F('stock') - item.quantity)
                    if not updated_stock:
                        raise ValidationError(f"Stock not available for {item.variant}")
                    Product.objects.filter(pk=item.product.pk).update(sold=F('sold') + item.quantity)
                else:
                    updated_stock = Product.objects.filter(
                        pk=item.product.pk,
                        stock__gte=item.quantity
                    ).update(
                        stock=F('stock') - item.quantity,
                        sold=F('sold') + item.quantity
                    )
                    if not updated_stock:
                        raise ValidationError(f"Stock not available for {item.product}")

            # --- Update totals & finalize checkout in one go ---
            Checkout.objects.filter(pk=self.pk).update(
                total_amount=subtotal,
                discount_amount=discount,
                final_amount=final_total,
                is_finalized=True,
                status='pending' if checkout.payment_method=='cod' else 'accepted',
                paid_at=None if checkout.payment_method=='cod' else timezone.now()
            )

    # ===============================
    # Restore stock & coupon
    # ===============================
    def restore_stock_and_coupon(self):
        with transaction.atomic():
            checkout = Checkout.objects.select_for_update().get(pk=self.pk)
            if not checkout.is_finalized:
                return

            items = checkout.items.select_related('product','variant').select_for_update()
            for item in items:
                if item.variant:
                    VariantOption.objects.filter(pk=item.variant.pk).update(
                        stock=F('stock') + item.quantity
                    )
                    Product.objects.filter(pk=item.product.pk).update(
                        sold=F('sold') - item.quantity
                    )
                else:
                    Product.objects.filter(pk=item.product.pk).update(
                        stock=F('stock') + item.quantity,
                        sold=F('sold') - item.quantity
                    )

            if checkout.coupon:
                Coupon.objects.filter(pk=checkout.coupon.pk, used_count__gt=0).update(
                    used_count=F('used_count') - 1
                )

            # Reset totals & finalize status in one go
            Checkout.objects.filter(pk=self.pk).update(
                total_amount=Decimal('0.00'),
                discount_amount=Decimal('0.00'),
                final_amount=Decimal('0.00'),
                is_finalized=False
            )


# =============================
# Checkout Item Model
# =============================
class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(VariantOption, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(_('unit_price'), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "04. Checkout Items"

    def save(self, *args, **kwargs):
        # Always recalc price & subtotal on save/update
        self.unit_price = self.variant.variant_price if self.variant else self.product.sale_price
        self.subtotal = (self.unit_price * self.quantity).quantize(Decimal('0.01'), ROUND_HALF_UP)
        super().save(*args, **kwargs)

    def __str__(self):
        variant = f" ({self.variant})" if self.variant else ""
        return f"{self.product.title}{variant} x {self.quantity} = {self.subtotal}"




    

