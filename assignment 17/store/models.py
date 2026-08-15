from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum, Min, Q
from decimal import Decimal
from store.validators import validate_image_size

User = get_user_model()

# =========================================================
# CHOICES
# =========================================================
STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)
VARIANTS_TYPE_CHOICES = (
    ('color', 'Color'),
    ('size', 'Size'),
    ('color-size', 'Color Size'),
    ('none', 'None'),
)
SLIDER_TYPE_CHOICES = (
    ('none', 'None'),
    ('slider', 'Slider'),
    ('add', 'Add'),
    ('feature', 'Feature'),
    ('promotion', 'Promotion'),
)

# =========================================================
# SLUG GENERATOR
# =========================================================
def generate_unique_slug(cls, title: str) -> str:
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while cls.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

# =========================================================
# IMAGE TAG MIXIN
# =========================================================
class ImageTagMixin(models.Model):
    class Meta:
        abstract = True

    def image_tag(self):
        img = getattr(self, 'image', None)
        if img and hasattr(img, 'url'):
            return mark_safe(f'<img src="{img.url}" style="max-width:50px; max-height:50px;" />')
        return mark_safe('<span>No Image</span>')

# =========================================================
# 01. CATEGORY MODEL
# =========================================================
class Category(ImageTagMixin):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    keyword = models.CharField(max_length=150, default='N/A')
    description = models.CharField(max_length=150, default='N/A')
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', default='defaults/default.jpg', validators=[validate_image_size])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01. Categories'

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.title) != self.slug:
            self.slug = generate_unique_slug(Category, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 02. BRAND MODEL
# =========================================================
class Brand(ImageTagMixin):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    keyword = models.CharField(max_length=150, default='N/A')
    description = models.CharField(max_length=150, default='N/A')
    image = models.ImageField(upload_to='brands/%Y/%m/%d/', default='defaults/default.jpg', validators=[validate_image_size])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '02. Brands'

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.title) != self.slug:
            self.slug = generate_unique_slug(Brand, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 03. COLOR MODEL
# =========================================================
class Color(ImageTagMixin):
    title = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['id']
        verbose_name_plural = '03. Product Colors'

    def __str__(self):
        return f"{self.title} ({self.code})"

    @property
    def color_tag(self):
        if self.code:
            return mark_safe(
                f'<div style="width:30px; height:30px; background-color:{self.code}; border:1px solid #000;"></div>'
            )
        return ""

# =========================================================
# 04. SIZE MODEL
# =========================================================
class Size(ImageTagMixin):
    title = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '04. Product Sizes'

    def __str__(self):
        return f"{self.title} ({self.code})"

# =========================================================
# 05 PRODUCT MODEL
# =========================================================
class Product(ImageTagMixin):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    variant = models.CharField(max_length=150, choices=VARIANTS_TYPE_CHOICES, default='none')
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)

    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('6000.00'))
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('4000.00'))
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(90)], default=Decimal('33.33'))
    available_stock = models.PositiveIntegerField(validators=[MaxValueValidator(10000)], default=1)
    sold = models.PositiveIntegerField(default=0)
    visited = models.PositiveIntegerField(default=0)

    prev_des = models.TextField(default='N/A')
    add_des = models.TextField(default='N/A')
    short_des = models.TextField(default='N/A')
    long_des = models.TextField(default='N/A')
    keyword = models.TextField(default='N/A')
    description = models.TextField(default='N/A')
    tag = models.CharField(max_length=150, default='N/A')

    deadline = models.DateTimeField(blank=True, null=True)
    is_deadline = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '05. Products'

    def save(self, *args, **kwargs):
        # automatic discount % calculate
        if self.old_price > 0:
            self.discount_percent = ((self.old_price - self.sale_price) / self.old_price) * 100
        super().save(*args, **kwargs)

    def clean(self):
        if self.is_deadline and self.deadline and self.deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past.")
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValidationError("Discount percent must be between 0 and 100.")
        

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 06. PRODUCT VARIANT MODEL
# =========================================================
class ProductVariant(ImageTagMixin):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, blank=True, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
    image_id = models.PositiveIntegerField(blank=True, null=True, default=0)
    sku = models.CharField(max_length=100, unique=True)
    variant_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    available_stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '06. Product Variants'

    def clean(self):
        if self.product.variant == 'color' and not self.color:
            raise ValidationError("This product requires a color variant.")
        if self.product.variant == 'size' and not self.size:
            raise ValidationError("This product requires a size variant.")
        if self.product.variant == 'color-size' and (not self.color or not self.size):
            raise ValidationError("This product requires both color and size.")
        if self.product.variant == 'none' and (self.color or self.size):
            raise ValidationError("This product does not use variants.")
    
    def get_image(self):
        image = ImageGallery.objects.filter(id=self.image_id, product=self.product).first()
        return image.image if image else None

    
    @property
    def image_url(self):
        img = self.get_image()
        return img.url if img else None

    @property
    def image_tag(self):
        img = self.get_image()
        if img and hasattr(img, 'url'):
            return mark_safe(f'<img src="{img.url}" style="max-width:50px; max-height:50px;" />')
        return mark_safe('<span>No Image</span>')

    def __str__(self):
        size = self.size.title if self.size else "No Size"
        color = self.color.title if self.color else "No Color"
        return f"({self.product.title}) - ({size} - {color})"

# =========================================================
# 07. IMAGE GALLERY MODEL
# =========================================================
class ImageGallery(ImageTagMixin):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galleries/%Y/%m/%d/', validators=[validate_image_size])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = '07. Image Galleries'

    def __str__(self):
        return f"{self.product.title} Image"

# =========================================================
# 08. SLIDER MODEL
# =========================================================
class Slider(ImageTagMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slider_type = models.CharField(max_length=10, choices=SLIDER_TYPE_CHOICES, default='none')
    title = models.CharField(max_length=150, unique=True)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    paragraph = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='sliders/%Y/%m/%d/', default='defaults/default.jpg', validators=[validate_image_size])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['id']
        verbose_name_plural = '08. Sliders'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 09. REVIEW MODEL
# =========================================================
class Review(ImageTagMixin):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=500)
    rating = models.FloatField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = '09. Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                condition=Q(status='active'),
                name='unique_active_review'
            )
        ]

    def __str__(self):
        return self.subject or f"Review by {self.user.username}"

# =========================================================
# 10. ACCEPTANCE PAYMENT MODEL
# =========================================================
class AcceptancePayment(ImageTagMixin):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='acceptance_payments/%Y/%m/%d/', default='defaults/default.jpg', validators=[validate_image_size])
    help_time = models.CharField(max_length=150, default="24/7 Support")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = '10. Acceptance Payments'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
