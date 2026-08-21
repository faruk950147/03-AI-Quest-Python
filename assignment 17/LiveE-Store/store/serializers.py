from rest_framework import serializers
from store.models import (
    StatusChoices,
    VariantType,
    SliderType,
    Category,
    Brand,
    Color,
    Size,
    Product,
    Gallery,
    VariantOption,
    Slider,
    Review,
    AllowPayment,
)

# ==================== CATEGORY ======================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id", "parent", "title", "slug", "image", "keyword", "description", 
            "created_at", "updated_at"
        )
        read_only_fields = ("slug", "created_at", "updated_at")
        
    def validate(self, attrs):
        title = attrs.get("title")
        if title and len(title.strip()) < 1:
            raise serializers.ValidationError({
                "title": "Category title cannot be empty."
            })
        return attrs
        
# ==================== BRAND ======================
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id", "title", "slug", "image", "keyword", "description", 
            "created_at", "updated_at"
        )
        read_only_fields = ("slug", "created_at", "updated_at")
        
    def validate(self, attrs):
        title = attrs.get("title")
        if title and len(title.strip()) < 1:
            raise serializers.ValidationError({
                "title": "Brand title cannot be empty."
            })
        return attrs
    
# ==================== COLOR ======================
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id", "title", "code", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
    
    def validate(self, attrs):
        title = attrs.get("title")
        code = attrs.get("code")

        if title and len(title.strip()) < 1:
            raise serializers.ValidationError({
                "title": "Color title cannot be empty."
            })

        if code and len(code.strip()) < 1:
            raise serializers.ValidationError({
                "code": "Color code cannot be empty."
            })

        return attrs

# ==================== SIZE ======================
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "title", "code", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
        
    def validate(self, attrs):
        title = attrs.get("title")
        code = attrs.get("code")

        if title and len(title.strip()) < 1:
            raise serializers.ValidationError({
                "title": "Size title cannot be empty."
            })

        if code and len(code.strip()) < 1:
            raise serializers.ValidationError({
                "code": "Size code cannot be empty."
            })

        return attrs

# ==================== PRODUCT ======================
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Product
        fields = (
            "id", "category", "brand", "variants_type", "title", "slug", "tag", 
            "old_price", "sale_price", "discount", "stock", "sold", "visited",
            "prev_des", "add_des", "short_des", "long_des", "keyword", "description",
            "deadline", "is_deadline", "is_featured", "status", "created_at", "updated_at"
        )
        read_only_fields = ("slug", "created_at", "updated_at")
        
    def validate(self, attrs):
        variants_type = attrs.get(
            "variants_type",
            self.instance.variants_type if self.instance else None
        )

        if variants_type not in dict(VariantType.choices):
            raise serializers.ValidationError({
                "variants_type": "Invalid variant type."
            })

        return attrs

# ===================== GALLERY ======================
class GallerySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Gallery
        fields = ("id", "product", "image", "status", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
        
    def validate(self, attrs):
        image = attrs.get("image")

        if not image:
            raise serializers.ValidationError({
                "image": "Image is required."
            })

        return attrs

# ===================== VARIANT OPTION =====================
class VariantOptionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    color = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        required=False,
        allow_null=True
    )
    size = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = VariantOption
        fields = (
            'id', 'product', 'color', 'size', 'sku', 'variant_price', 'stock', 'status',
            'created_at', 'updated_at'
        )
        read_only_fields = ("created_at", "updated_at")
    
    def validate(self, attrs):
        product = attrs.get(
            "product",
            self.instance.product if self.instance else None
        )

        color = attrs.get(
            "color",
            self.instance.color if self.instance else None
        )

        size = attrs.get(
            "size",
            self.instance.size if self.instance else None
        )

        if product.variants_type == VariantType.COLOR:
            if not color:
                raise serializers.ValidationError({
                    "color": "Color is required."
                })

        elif product.variants_type == VariantType.SIZE:
            if not size:
                raise serializers.ValidationError({
                    "size": "Size is required."
                })

        elif product.variants_type == VariantType.COLOR_SIZE:
            if not color or not size:
                raise serializers.ValidationError({
                    "non_field_errors":
                    "Both color and size are required."
                })

        elif product.variants_type == VariantType.NONE:
            if color or size:
                raise serializers.ValidationError({
                    "non_field_errors":
                    "This product does not use variants."
                })

        return attrs

# ====================== SLIDER ======================
class SliderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Slider
        fields = (
            'id', 'product', 'slider_type', 'headline', 'paragraph', 'image', 'status', 
            'created_at', 'updated_at'
        )
        read_only_fields = ("created_at", "updated_at")
        
    def validate(self, attrs):
        slider_type = attrs.get(
            "slider_type",
            self.instance.slider_type if self.instance else None
        )

        if slider_type not in dict(SliderType.choices):
            raise serializers.ValidationError({
                "slider_type": "Invalid slider type."
            })

        return attrs
        
# ====================== REVIEW ======================
class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'product', 'user', 'subject', 'comment', 'rating', 'status',
            'created_at', 'updated_at'
        )
        read_only_fields = ("created_at", "updated_at")
        
    def validate(self, attrs):
        rating = attrs.get("rating")

        if rating is not None and (rating < 1 or rating > 5):
            raise serializers.ValidationError({
                "rating": "Rating must be between 1 and 5."
            })

        return attrs

# ===================== ALLOW PAYMENT ======================
class AllowPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowPayment
        fields = (
            'id', 'title', 'help_time', 'image', 'status', 'created_at', 'updated_at'
        )
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        title = attrs.get("title")
        if title and len(title.strip()) < 3:
            raise serializers.ValidationError({
                "title": "Title must be at least 3 characters long."
            })
        return attrs
    


