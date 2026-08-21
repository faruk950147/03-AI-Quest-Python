from rest_framework import serializers

from cart.models import Cart
from store.models import Product, VariantOption, StatusChoices


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status=StatusChoices.Active),
    )
    variant = serializers.PrimaryKeyRelatedField(
        queryset=VariantOption.objects.filter(status=StatusChoices.Active),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Cart
        fields = [
            "id", "user", "product", "variant", "quantity", "paid", "stored_unit_price", "created_at", "updated_at",
        ]

        read_only_fields = [
            "id", "user", "paid", "stored_unit_price", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        product = attrs.get("product")
        variant = attrs.get("variant")
        quantity = attrs.get("quantity")

        if variant:
            if variant.stock < quantity:
                raise serializers.ValidationError({
                    "quantity": "Not enough stock."
                })
        else:
            if product.stock < quantity:
                raise serializers.ValidationError({
                    "quantity": "Not enough stock."
                })

        return attrs
    
    
class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status=StatusChoices.Active),
    )
    variant = serializers.PrimaryKeyRelatedField(
        queryset=VariantOption.objects.filter(status=StatusChoices.Active),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Cart
        fields = [
            "id", "user", "product", "variant", "created_at", "updated_at",
        ]

        read_only_fields = [
            "id", "user", "created_at", "updated_at",
        ]   