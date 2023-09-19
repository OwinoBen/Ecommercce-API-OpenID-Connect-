from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_title', 'product_sku', 'product_qty', 'selling_price', 'discount_price', 'image',
                  'is_verified', 'created_date']
        read_only_fields = ('id', 'product_sku', 'created_date')

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        updated_fields = [k for k in validated_data]
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save(update_fields=updated_fields)
        return instance
