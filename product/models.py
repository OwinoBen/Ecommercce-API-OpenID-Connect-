import uuid
import random

from django.db import models
from util.helper import image_path


class Product(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    product_title = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=100, blank=True)
    product_qty = models.IntegerField(default=0)
    selling_price = models.FloatField(max_length=10)
    discount_price = models.FloatField(max_length=255, default=0.0, blank=True, null=True)
    image = models.ImageField(upload_to=image_path, blank=True, null=True, default='')
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        sku = 'SKU' + str(random.randint(1, 1000000))
        self.product_sku = sku
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Product, self).delete(*args, **kwargs)

    def __str__(self):
        return "%s" % self.id
