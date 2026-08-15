import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Sum, F
from checkout.models import Checkout
from cart.models import Cart
from accounts.models import Profile
User = get_user_model()
logger = logging.getLogger('project')

@method_decorator(never_cache, name='dispatch')
class CheckoutView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')
    def get(self, request):
        checkout_items = Cart.objects.filter(user=request.user, paid=False).select_related("product")
        summary = checkout_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))
        shipping_cost = 120
        grand_total = (summary['total_price'] or 0) + shipping_cost
        profiles = Profile.objects.filter(user=request.user)

        logger.info(f"User {request.user.username} visited checkout page. Items count: {checkout_items.count()}, Grand total: {grand_total}")

        context = {
            "checkout_items": checkout_items,
            "shipping_cost": shipping_cost,
            "grand_total": grand_total,
            "profiles": profiles,
        }
        return render(request, 'checkout/checkout.html', context)


@method_decorator(never_cache, name='dispatch')
class CheckoutSuccessView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def post(self, request):
        address_id = request.POST.get('address-id')

        if not address_id:
            logger.warning(f"User {request.user.username} tried to checkout without selecting address.")
            return redirect('checkout')

        profile = get_object_or_404(Profile, id=address_id, user=request.user)

        cart_items = Cart.objects.filter(user=request.user, paid=False)
        if not cart_items.exists():
            logger.warning(f"User {request.user.username} tried to checkout with empty cart.")
            return redirect('checkout')

        for item in cart_items:
            Checkout.objects.create(
                user=request.user,
                profile=profile,
                product=item.product,
                quantity=item.quantity,
                status='Pending',
                is_ordered=True
            )
            logger.info(f"User {request.user.username} ordered Product {item.product.id} - {item.product.title}, quantity: {item.quantity}")

        cart_items.update(paid=True)
        cart_items.delete()

        logger.info(f"User {request.user.username} completed checkout successfully. Total items: {cart_items.count()}")

        return redirect('checkout-list')


@method_decorator(never_cache, name='dispatch')
class CheckoutListView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign-in')

    def get(self, request):
        checkout_items = Checkout.objects.filter(user=request.user, is_ordered=True).order_by('-ordered_date').select_related('product', 'profile')
        grand_total = checkout_items.aggregate(total_price=Sum(F("quantity") * F("product__sale_price")))['total_price'] or 0

        logger.info(f"User {request.user.username} visited checkout list page. Orders count: {checkout_items.count()}")
        return render(request, 'checkout/checkout_list.html', {
            'checkout_items': checkout_items
        })
