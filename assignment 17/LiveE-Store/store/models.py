from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    ValidationError,
)
from django.utils import timezone
from django.utils.html import format_html

from mixins.mixing import ImageTagMixin, ColorTagMixin

from validation.validators import validate_file_extension, validate_image_size

User = get_user_model()

# ======================== CONSTANTS ========================


# ======================== STATUS ========================
class StatusChoices(models.TextChoices):
    Active = "active", _("Active")
    Inactive = "inactive", _("Inactive")


# ======================== VARIANT TYPE ========================
class VariantType(models.TextChoices):
    NONE = "none", _("None")
    COLOR = "color", _("Color")
    SIZE = "size", _("Size")
    COLOR_SIZE = "color_size", _("Color Size")


# ======================== SLIDER TYPE ========================
class SliderType(models.TextChoices):
    NONE = "none", _("None")
    SLIDER = "slider", _("Slider")
    ADD = "add", _("Add")
    FEATURE = "feature", _("Feature")
    PROMOTION = "promotion", _("Promotion")


# ======================== BASE MIXIN ========================
class BaseMixin(models.Model):
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.Active,
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    class Meta:
        abstract = True


# ======================== COMMON MIXIN ========================
class CommonMixin(models.Model):
    slug = models.SlugField(_("slug"), max_length=255, unique=True, blank=True, null=True)
    keyword = models.CharField(_("keyword"), max_length=255, blank=True, null=True)
    description = models.CharField(_("description"), max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            # title field parent model 
            if hasattr(self, "title"):
                base_slug = slugify(self.title)
            else:
                base_slug = slugify(str(self))

            self.slug = base_slug

        super().save(*args, **kwargs)


# ======================== CATEGORY ========================
class Category(BaseMixin, CommonMixin, ImageTagMixin):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    title = models.CharField(_("title"), max_length=255, unique=True)
    image = models.ImageField(
        _("image"),
        upload_to="categories/%Y/%m/%d/",
        validators=[validate_image_size, validate_file_extension],
        default="defaults/default.jpg"
    )
    icon = models.CharField(_("icon"), max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(_("is_featured"), default=False)

    class Meta:
        verbose_name_plural = "01. Categories"
        db_table = "store_categories"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
        ]

    def clean(self):
        if self.parent and self.parent.parent and self.parent.parent.parent:
            raise ValidationError("Maximum 3 levels allowed")

    def __str__(self):
        return f"{self.title}"


# ======================== BRAND ========================
class Brand(BaseMixin, CommonMixin, ImageTagMixin):
    title = models.CharField(_("title"), max_length=255, unique=True)
    image = models.ImageField(
        _("image"),
        upload_to="brands/%Y/%m/%d/",
        validators=[validate_image_size, validate_file_extension],
        default="defaults/default.jpg"
    )
    is_featured = models.BooleanField(_("is_featured"), default=False)

    class Meta:
        verbose_name_plural = "02. Brands"
        db_table = "store_brands"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.title}"


# ======================== COLOR ========================
class Color(BaseMixin, ColorTagMixin):
    title = models.CharField(_("title"), max_length=255, unique=True)
    code = models.CharField(_("code"), max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "03. Colors"
        db_table = "store_colors"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.title}"


# ======================== SIZE ========================
class Size(BaseMixin):
    title = models.CharField(_("title"), max_length=255, unique=True)
    code = models.CharField(_("code"), max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "04. Sizes"
        db_table = "store_sizes"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.title}"


# ======================== PRODUCT ========================
class Product(BaseMixin, CommonMixin, ImageTagMixin):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    variants_type = models.CharField(
        max_length=20,
        choices=VariantType.choices,
        default=VariantType.NONE,
    )

    title = models.CharField(_("title"), max_length=255, unique=True)
    tag = models.CharField(_("tag"), max_length=150, blank=True, null=True)

    old_price = models.DecimalField(_("old_price"), max_digits=10, decimal_places=2, default=Decimal("0.00"))
    sale_price = models.DecimalField(_("sale_price"), max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(_("discount"), max_digits=10, decimal_places=2, default=Decimal("0.00"))

    stock = models.PositiveIntegerField(_("stock"), default=0, validators=[MaxValueValidator(10000)])
    sold = models.PositiveIntegerField(_("sold"), default=0)
    visited = models.PositiveIntegerField(_("visited"), default=0)

    prev_des = models.TextField(blank=True, null=True)
    add_des = models.TextField(blank=True, null=True)
    short_des = models.TextField(blank=True, null=True)
    long_des = models.TextField(blank=True, null=True)

    deadline = models.DateTimeField(_("deadline"), blank=True, null=True)
    is_deadline = models.BooleanField(_("is_deadline"), default=False)
    is_featured = models.BooleanField(_("is_featured"), default=False)

    class Meta:
        verbose_name_plural = "05. Products"
        db_table = "store_products"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["old_price"]),
            models.Index(fields=["sale_price"]),
            models.Index(fields=["discount"]),
            models.Index(fields=["stock"]),
            models.Index(fields=["sold"]),
            models.Index(fields=["visited"]),
            models.Index(fields=["is_deadline"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["status"])
        ]

    def calculate_discount(self):
        if self.old_price and self.sale_price and self.old_price > 0:
            if self.sale_price < self.old_price:
                self.discount = (
                    (self.old_price - self.sale_price) / self.old_price * 100
                ).quantize(Decimal("0.01"))
            else:
                self.discount = Decimal("0.00")

    def clean(self):
        if self.is_deadline and self.deadline and self.deadline < timezone.now():
            raise ValidationError("Deadline cannot be in past")

        if self.sale_price > self.old_price:
            raise ValidationError("Sale price cannot be greater than old price")

    def save(self, *args, **kwargs):
        self.calculate_discount()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.title}"


# ======================== GALLERY ========================
class Gallery(BaseMixin, ImageTagMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="galleries")
    image = models.ImageField(
        _("image"), 
        upload_to="products/gallery/%Y/%m/%d/", 
        validators=[validate_image_size, validate_file_extension],
        default="defaults/default.jpg"
    )

    class Meta:
        verbose_name_plural = "06. Galleries"
        db_table = "store_galleries"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.product.title}"


# ======================== VARIANT OPTION ========================
class VariantOption(BaseMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)

    image_id = models.PositiveIntegerField(_("image_id"), null=True, blank=True, default=0)

    sku = models.CharField(_("sku"), max_length=100, unique=True)
    variant_price = models.DecimalField(_("variant_price"), max_digits=10, decimal_places=2, default=Decimal("0.00"))
    stock = models.PositiveIntegerField(_("stock"), default=0)

    class Meta:
        verbose_name_plural = "07. Variant Options"
        db_table = "store_variant_options"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["variant_price"]),
            models.Index(fields=["stock"]),
        ]

    def clean(self):
        vt = self.product.variants_type

        if vt == VariantType.COLOR and not self.color:
            raise ValidationError("Color required")

        if vt == VariantType.SIZE and not self.size:
            raise ValidationError("Size required")

        if vt == VariantType.COLOR_SIZE:
            if not self.color or not self.size:
                raise ValidationError("Color + Size required")

        if vt == VariantType.NONE and (self.color or self.size):
            raise ValidationError("No variant allowed")

    def get_image(self):
        image = Gallery.objects.filter(id=self.image_id, product=self.product).first()

        if image:
            return image.image
        return None

    @property
    def image_url(self):
        img = self.get_image()
        return img.url if img else None

    @property
    def image_tag(self):
        img = self.get_image()
        if img:
            return format_html('<img src="{}" width="30" height="30"/>', img.url)
        return "No Image"

    def __str__(self):
        return f"{self.product.title}"


# ======================== SLIDER ========================
class Slider(BaseMixin, ImageTagMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sliders")
    slider_type = models.CharField(_('slider_type'), max_length=20, choices=SliderType.choices)
    headline = models.CharField(_('headline'), max_length=150, blank=True, null=True)
    button = models.CharField(_('button'), max_length=150, blank=True, null=True)

    image = models.ImageField(
        _('image'), 
        upload_to="sliders/%Y/%m/%d/", 
        validators=[validate_image_size, validate_file_extension],
        default="defaults/default.jpg"
    )

    class Meta:
        verbose_name_plural = "08. Sliders"
        db_table = "store_sliders"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["slider_type"]),
        ]

    def __str__(self):
        return f"{self.product.title}"


# ======================== REVIEW ========================
class Review(BaseMixin, ImageTagMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(_('subject'), max_length=50)
    comment = models.TextField(_('comment'), max_length=500)
    rating = models.DecimalField(
        _('rating'),
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    class Meta:
        verbose_name_plural = "09. Reviews"
        db_table = "store_reviews"
        ordering = ["id"]
        
        # indexing for faster queries
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.subject}"


# ======================== PAYMENT ========================
class AllowPayment(BaseMixin, ImageTagMixin):
    title = models.CharField(_('title'), max_length=150, unique=True)
    help_time = models.CharField(_('help_time'), max_length=150, default="24/7 Support")

    image = models.ImageField(
        _('image'), 
        upload_to="allows_payments/%Y/%m/%d/", 
        validators=[validate_image_size, validate_file_extension],
        default="defaults/default.jpg"
    )

    is_featured = models.BooleanField(_('is_featured'), default=False)

    class Meta:
        verbose_name_plural = "10. Allow Payments"
        db_table = "store_allow_payments"
        ordering = ["id"]

        # indexing for faster queries
        indexes = [
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return f"{self.title}"