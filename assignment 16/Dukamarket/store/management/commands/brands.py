from django.core.management.base import BaseCommand
from store.models import Brand

class Command(BaseCommand):
    help = "Seed predefined product brands into the database"

    brands = [
        ("Duka", "Fashion brand for all"),
        ("Men", "Men's clothing brand"),
        ("Gap", "International lifestyle brand"),
        ("Zara", "Trendy fashion brand"),
        ("H&M", "Global fashion retailer"),
    ]

    def handle(self, *args, **kwargs):
        for title, description in self.brands:
            brand, created = Brand.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "keyword": title.lower(),
                    "status": "active",
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Brand Added: {title}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Brand Already Exists: {title}"))

        self.stdout.write(self.style.SUCCESS("Brand seeding completed!"))
