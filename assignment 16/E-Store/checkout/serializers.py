from rest_framework import serializers

from store.models import Product, VariantOption
from checkout.models import Coupon, Checkout, CheckoutItem, Shipping


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'discount_percent', 'max_usage', 'used_count', 'max_discount_amount', 
            'active', 'start_date', 'end_date', 'created_at', 'updated_at',
        ]
        read_only_fields = (
            'used_count',
            'created_at',
            'updated_at',
        )


class CheckoutSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    coupon = serializers.PrimaryKeyRelatedField(
        queryset=Coupon.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Checkout
        fields = [
            'id', 'user', 'coupon', 'payment_method', 'status', 'is_finalized', 'paid_at',
            'total_amount', 'discount_amount', 'final_amount', 'created_at', 'updated_at',
        ]
        read_only_fields = (
            'status',
            'is_finalized',
            'paid_at',
            'total_amount',
            'discount_amount',
            'final_amount',
            'created_at',
            'updated_at',
        )

    def validate_coupon(self, value):
        if value is None:
            return value

        request = self.context.get("request")
        user = request.user if request else None

        valid, message = value.is_valid(user=user)
        if not valid:
            raise serializers.ValidationError(message)

        return value


class CheckoutItemSerializer(serializers.ModelSerializer):
    checkout = serializers.PrimaryKeyRelatedField(
        queryset=Checkout.objects.all()
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    variant = serializers.PrimaryKeyRelatedField(
        queryset=VariantOption.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CheckoutItem
        fields = [
            'id', 'checkout', 'product', 'variant', 'quantity', 'unit_price', 
            'subtotal', 'created_at', 'updated_at',
        ]
        read_only_fields = (
            'unit_price',
            'subtotal',
            'created_at',
            'updated_at',
        )

    def validate(self, attrs):
        checkout = attrs.get("checkout")
        product = attrs.get("product")
        variant = attrs.get("variant")
        quantity = attrs.get("quantity")

        # Checkout ownership
        request = self.context.get("request")
        if request and checkout.user != request.user:
            raise serializers.ValidationError(
                {"checkout": "Invalid checkout."}
            )

        # Variant belongs to product
        if variant and variant.product_id != product.id:
            raise serializers.ValidationError(
                {"variant": "Variant does not belong to the selected product."}
            )

        # Stock validation
        if variant:
            if quantity > variant.stock:
                raise serializers.ValidationError(
                    {
                        "quantity": f"Only {variant.stock} item(s) available in stock."
                    }
                )
        else:
            if quantity > product.stock:
                raise serializers.ValidationError(
                    {
                        "quantity": (
                            f"Only {product.stock} item(s) available in stock."
                        )
                    }
                )

        return attrs


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = [
            'id', 'user', 'shipping_choice', 'name', 'country', 'city', 'home_city', 'zip_code', 'phone', 
            'address', 'created_at', 'updated_at',
        ]
        read_only_fields = (
            'created_at',
            'updated_at',
        )
        
        def validate(self, attrs):
            shipping_choice = attrs.get("shipping_choice")
            country = attrs.get("country")
            city = attrs.get("city")
            home_city = attrs.get("home_city")
            zip_code = attrs.get("zip_code")
            phone = attrs.get("phone")
            address = attrs.get("address")

            if shipping_choice == Shipping.SHIPPING_CHOICES[0][0]:  # Home Delivery
                if not all([country, city, home_city, zip_code, phone, address]):
                    raise serializers.ValidationError(
                        {
                            "shipping_choice": "All fields are required for Home Delivery."
                        }
                    )
            elif shipping_choice == Shipping.SHIPPING_CHOICES[1][0]:  # Store Pickup
                if not all([name, phone]):
                    raise serializers.ValidationError(
                        {
                            "shipping_choice": "Name and Phone are required for Store Pickup."
                        }
                    )

            return attrs