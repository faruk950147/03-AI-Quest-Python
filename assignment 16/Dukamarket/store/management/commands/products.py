from django.core.management.base import BaseCommand
from store.models import Category, Brand, Product

class Command(BaseCommand):
    help = "Seed predefined products with categories and brands into the database"

    # ==========================
    # Products + category + brand
    # ==========================
    products = [
        # Lehenga (Women Clothing → Lehenga)
        ("Paithani Lehenga Dark Red", "Lehenga", "SareeHouse"),
        ("Banarasi Lehenga Bright Red", "Lehenga", "SareeHouse"),
        ("Rajasthani Lehenga Silver Pink", "Lehenga", "SareeHouse"),
        ("Kanjeevaram Lehenga Cool Slate Gray", "Lehenga", "SareeHouse"),
        ("Fabric-Based Lehengas Dark Navy", "Lehenga", "SareeHouse"),

        # T-Shirt (Men Clothing → T-Shirt)
        ("Crew Neck T-Shirt Sweet Pink", "T-Shirt", "Nike"),
        ("V-Neck T-Shirt Dark Navy", "T-Shirt", "Nike"),
        ("Round Neck T-Shirt Cool Slate Gray", "T-Shirt", "Adidas"),
        ("Polo T-Shirt Dark Red", "T-Shirt", "Polo"),
        ("Scoop Neck T-Shirt Ocean Blue", "T-Shirt", "Puma"),

        # Laptops (Electronics → Laptop)
        ("MacBook Pro 14” / 16”", "Laptop", "Apple"),
        ("Dell XPS 15", "Laptop", "Dell"),
        ("HP Spectre x360", "Laptop", "HP"),
        ("Lenovo Yoga 9i", "Laptop", "Lenovo"),
        ("Microsoft Surface Laptop", "Laptop", "Microsoft"),

        # Mobiles (Electronics → Mobile)
        ("Samsung Galaxy A54", "Mobile", "Samsung"),
        ("Xiaomi Redmi Note 13 / Note 12", "Mobile", "Xiaomi"),
        ("Realme 12 / 11", "Mobile", "Realme"),
        ("Vivo V30 / Y100", "Mobile", "Vivo"),
        ("OPPO Reno 10 / OPPO A Series", "Mobile", "OPPO"),
    ]

    def handle(self, *args, **kwargs):
        for title, category_title, brand_title in self.products:
            # ==========================
            # Get category
            # ==========================
            category_qs = Category.objects.filter(title=category_title)
            if not category_qs.exists():
                self.stdout.write(self.style.ERROR(f"Category '{category_title}' does not exist for product '{title}'"))
                continue
            category = category_qs[0]

            # ==========================
            # Get brand
            # ==========================
            brand_qs = Brand.objects.filter(title=brand_title)
            if not brand_qs.exists():
                # Create brand if it doesn't exist
                brand = Brand.objects.create(title=brand_title)
                self.stdout.write(self.style.SUCCESS(f"Created brand: {brand_title}"))
            else:
                brand = brand_qs[0]

            # ==========================
            # Create or get product
            # ==========================
            product, created = Product.objects.get_or_create(
                title=title,
                defaults={
                    "category": category,
                    "brand": brand,
                }
            )

            # If product exists but category/brand is different, update it
            if not created:
                updated = False
                if product.category != category:
                    product.category = category
                    updated = True
                if product.brand != brand:
                    product.brand = brand
                    updated = True
                if updated:
                    product.save()

            action = "Created" if created else "Updated/Exists"
            self.stdout.write(f"{action} product: {title}")
