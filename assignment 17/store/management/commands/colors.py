import requests
from django.core.management.base import BaseCommand
from store.models import Color

class Command(BaseCommand):
    help = "Seed predefined product colors into the database"

    COLORS = [
        ("Silver Pink", "#C2ACA5"),
        ("Dark Navy", "#040812"),
        ("Cool Slate Gray", "#84878F"),
        ("Slate Gray", "#918A80"),
        ("Dark Red", "#8C081B"),
        ("Green", "#518680"),
        ("Dark Spring Green", "#0D693C"),
        ("Rosy Brown", "#C59478"),
        ("Ocean Blue", "#1E8BBB"),
        ("Sweet Pink", "#EF616A"),
        ("Verdigris", "#50B0A4"),
        ("Brownish Orange", "#895B3A"),
        ("Muted Purple", "#714B74"),
        ("Warm Grey", "#D5CBC5"),
        ("Raisin Black", "#1C1F23"),
        ("Cold Purple", "#8473B4"),
        ("Shadow Aqua", "#91ACAF"),
        ("Ash Grey", "#C5C0BA"),
        ("Bright Red", "#DD011E"),
        ("Black", "#000000"),
    ]

    def handle(self, *args, **kwargs):
        for title, code in self.COLORS:
            color, created = Color.objects.get_or_create(
                title=title,
                defaults={"code": code, "status": "active"}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Color: {title} ({code})"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {title} ({code})"))

        self.stdout.write(self.style.SUCCESS("All colors processed successfully!"))
