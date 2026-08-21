from settings.models import (
    Logo,
    Menubar,
    Footer,
    Copyright,
    SocialLink,
    StatusChoices,
)


def settings_context(request):
    return {
        "logo": Logo.objects.filter(
            status=StatusChoices.ACTIVE
        ).first(),

        "menubars": Menubar.objects.filter(
            status=StatusChoices.ACTIVE,
            parent__isnull=True,
        ).prefetch_related("children"),

        "footer": Footer.objects.filter(
            status=StatusChoices.ACTIVE
        ).first(),

        "copyright": Copyright.objects.filter(
            status=StatusChoices.ACTIVE
        ).first(),

        "social_links": SocialLink.objects.filter(
            status=StatusChoices.ACTIVE
        ),
    }