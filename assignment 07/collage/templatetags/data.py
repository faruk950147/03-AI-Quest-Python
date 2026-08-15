from django import template
register = template.Library()

@register.filter
def course(name):
    return f"Python Django {name}!"
