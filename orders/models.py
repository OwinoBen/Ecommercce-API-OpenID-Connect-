import datetime
import math
import random
import uuid

from django.db import models
from django.db.models import Sum, Avg, Count
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from product.models import Product
from util.regex_validator.regex import alphanumeric, numericValidator, charValidator

User = get_user_model()


class OrderManagementQuerySet(models.QuerySet):
    def recent_orders(self):
        return self.order_by('-updated_at', '-created_at')

    def getSells_breakdown(self):
        recent = self.recent_orders().not_refunded()
        recent_orders = recent.recent_orders()
        recent_cart_data = recent.get_cartData()
        shipped = recent.not_refunded().get_order_by_status(order_status='shipped')
        shipped_orders = shipped.order_total()
        paid = recent.get_order_by_status(order_status='paid')
        paid_orders = paid.order_total()

        data = {
            'recent': recent,
            'recent_orders': recent_orders,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_orders': shipped_orders,
            'paid': paid,
            'paid_orders': paid_orders
        }

        return data

    def not_refunded(self):
        return self.exclude(order_status='refunded')

    def get_orders_by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.get_order_by_range(start_date, end_date=end_date)

    def get_order_by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated_at__gte=start_date)
        return self.filter(updated_at__gte=start_date).filter(updated_at__lte=end_date)

    def get_order_by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated_at__day__gte=now.day)

    def order_total(self):
        return self.aggregate(Sum("amount"), Avg("amount"))

    def get_cart_data(self):
        return self.aggregate(
            Sum("items__product__discount_price"),
            Avg("items__product__discount_price"),
            Count("items__product")
        )

    def get_order_by_status(self, status='shipped'):
        return self.filter(order_status=status)

    def get_not_created_orders(self):
        return self.exclude(order_status='created')


class OrderManager(models.Manager):
    def new(self, customer=None):
        customer_object = None
        if customer is not None and customer.is_authenticated:
            customer_object = customer
        return self.model.objects.create(customer=customer_object)

    def get_queryset(self):
        return OrderManagementQuerySet(self.model, using=self._db)

    def get_sells_breakdown(self):
        return self.get_queryset().getSells_breakdown()

    def get_order_by_range(self, start_date, end_date=None):
        return self.get_queryset().get_order_by_range(start_date, end_date)

    def get_orders_by_weeks_range(self, weeks_ago, number_of_weeks):
        return self.get_queryset().get_orders_by_weeks_range(weeks_ago=weeks_ago, number_of_weeks=number_of_weeks)


class Orders(models.Model):
    STATUS = (
        ('ordered', 'Ordered'),
        ('refunded', 'Refunded order'),
        ('shipped', 'On shipping'),
        ('received', 'Order received'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order_id = models.CharField(_("Order ID"), max_length=125, unique=True, blank=True, validators=[alphanumeric])
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    amount = models.FloatField(_("Order Amount"), default=0.00)
    order_status = models.CharField(_("Order status"), max_length=120, default='ordered', choices=STATUS)
    active = models.BooleanField(_("Order active"), default=True)
    payment_mode = models.CharField(_("Mode of payment"), max_length=255, blank=True, validators=[charValidator])
    created_at = models.DateTimeField(_("Order date order was uploaded"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated on"), auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        order_id = 'ORD' + str(random.randint(1, 1000000))
        self.order_id = order_id
        super().save(*args, **kwargs)

    def get_sub_total(self):
        subtotal = 0
        for items in self.items.all():
            subtotal += items.getTotalItemPrice()
        return subtotal

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_order_amount()
        return total

    def get_absoluteUrl(self):
        return reverse("order:orders-detail", kwargs={'order_id': self.order_id})

    def get_status(self) -> str:
        if self.order_status == 'refunded':
            return 'Refunded order'
        elif self.order_status == 'shipped':
            return "Shipped"
        return 'Shipping soon'

    def update_total(self):
        cart_total = self.get_total()
        new_total = math.fsum([cart_total])
        formatted_total = format(new_total, '.2f')
        self.amount = formatted_total
        self.save()
        return new_total

    def update_purchased_product(self):
        for item in self.items.all():
            bj, created = PurchasedProducts.objects.get_or_create(
                order=self.order_id,
                product=item
            )
            return PurchasedProducts.objects.filter(order=self.order_id).count()

    def mark_paid(self):
        if self.order_status != 'paid':
            self.order_status = 'paid'
            self.save()
            self.update_purchased_product()
        return self.order_status


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="items")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer',
                                 blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order Items'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity} of {self.product.product_title}"

    def save(self, *args, **kwargs):
        self.order.amount = self.get_final_order_amount()
        super().save(*args, **kwargs)

    def get_total_item_price(self) -> float:
        return self.quantity * self.product.selling_price

    def get_total_discount_price(self) -> float:
        return self.quantity * self.product.discount_price

    def get_order_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_order_amount(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


class PurchasedProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)


class PurchasedProductManager(models.Manager):
    def get_queryset(self):
        return PurchasedProductQuerySet(self.model, using=self._db)

    def get_all(self):
        return self.get_queryset().active()


class PurchasedProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    refunded = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    object = PurchasedProductManager

    class Meta:
        verbose_name = 'Purchased Products'
        verbose_name_plural = 'Purchased Products'

    def __str__(self):
        return self.product.product_title
