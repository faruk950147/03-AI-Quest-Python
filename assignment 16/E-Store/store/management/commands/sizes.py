from django.core.management.base import BaseCommand
from store.models import Size

class Command(BaseCommand):
    help = "Seed predefined product sizes into the database"

    SIZES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]

    def handle(self, *args, **kwargs):
        for title, code in self.SIZES:
            size, created = Size.objects.get_or_create(
                title=title,
                defaults={"code": code, "status": "active"}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Size: {title} ({code})"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {title} ({code})"))

        self.stdout.write(self.style.SUCCESS("All sizes processed successfully!"))
