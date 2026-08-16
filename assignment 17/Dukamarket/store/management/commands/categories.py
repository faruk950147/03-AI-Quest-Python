from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = "Seed predefined product categories into the database"

    # You can define parent-child relationships here if needed
    categories = [
        ("Clothing", None),
        ("Women Clothing", "Clothing"),
        ("Men Clothing", "Clothing"),
        ("Lehenga", "Women Clothing"),
        ("T-Shirt", "Men Clothing"),
    ]

    def handle(self, *args, **kwargs):
        for title, parent_title in self.categories:
            # Find parent category object if parent_title exists
            parent = None
            if parent_title:
                parent = Category.objects.filter(title=parent_title).first()

            # Create or get the category
            category, created = Category.objects.get_or_create(
                title=title,
                defaults={"parent": parent}
            )

            # If category exists but parent is missing, update it
            if not created and parent and category.parent != parent:
                category.parent = parent
                category.save()

            action = "Created" if created else "Exists"
            self.stdout.write(f"{action} category: {title}")
