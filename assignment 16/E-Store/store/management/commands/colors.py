from django.core.management.base import BaseCommand
from store.models import Color


class Command(BaseCommand):
    help = "Seed predefined product colors into the database"

    COLORS = [
        ("Silver Pink", "#C2ACA5"),
        ("Dark Navy", "#000033"),
        ("Cool Slate Gray", "#84878F"),
        ("Dark Red", "#8C081B"),
        ("Green", "#518680"),
        ("Dark Spring Green", "#0D693C"),
        ("Rosy Brown", "#C59478"),
        ("Ocean Blue", "#1E8BBB"),
        ("Sweet Pink", "#EF616A"),
        ("Verdigris", "#50B0A4"),
        ("Brownish Orange", "#895B3A"),
        ("Black", "#000000"),
        ("White", "#ffffff"),
    ]

    def handle(self, *args, **kwargs):
        for title, code in self.COLORS:
            color, created = Color.objects.get_or_create(
                title=title,
                defaults={
                    "code": code,
                    "status": "active",
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Color: {title} ({code})"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {title} ({code})"))

        self.stdout.write(self.style.SUCCESS("All colors processed successfully!"))