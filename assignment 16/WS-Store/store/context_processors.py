from django.db.models import Min, Max
from store.models import (
    Category,
)
def get_filters(request):
    categories = Category.objects.filter(status='ACTIVE')
    return {
        'categories': categories,
    }