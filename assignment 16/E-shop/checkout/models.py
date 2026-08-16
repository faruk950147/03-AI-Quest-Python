from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Profile
from store.models import Product

User = get_user_model()

class Checkout(models.Model):
    STATUS_CHOICE = (
        ('Pending', 'Pending'),
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On the Way', 'On the Way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')

    is_ordered = models.BooleanField(default=False)    

    ordered_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.quantity * self.product.sale_price

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
