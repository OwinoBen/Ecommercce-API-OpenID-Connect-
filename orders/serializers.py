from rest_framework import serializers

from util.messages.response_SMS import send_sms_notification
from product.models import Product
from .models import Orders, OrderItems


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='product_title')
    item = serializers.UUIDField(write_only=True)

    class Meta:
        model = OrderItems
        fields = ['product', 'item', 'ordered', 'quantity', 'updated_at', 'created_at']
        read_only_fields = ('created_at', 'product')

    def product_title(self, obj):
        return obj.product.product_title


class CustomSerializer(serializers.Serializer):
    order_status = serializers.SerializerMethodField(method_name='order_status')
    amount = serializers.SerializerMethodField(method_name='order_amount')
    customer = serializers.SerializerMethodField(method_name='customer_full_name')


class OrderSerializer(serializers.ModelSerializer, CustomSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Orders

        fields = ['id', 'order_id', "order_status", 'active', 'customer', 'payment_mode', 'items', 'amount',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'order_id', 'active', 'customer', 'created_at', 'updated_at']

    def customer_full_name(self, obj):
        """Return Order Total amount with shipping or tax fee"""
        return obj.customer.get_full_name()

    def order_amount(self, obj):
        return obj.get_total()

    def order_status(self, obj):
        """Return Order status"""
        return self.Meta.model.STATUS[obj.order_status][1]

    def create(self, validated_data):
        """Implement order uploading logic and send sms notification to the customer"""
        user = None
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user = request.user

        if 'items' in validated_data:
            order_items = validated_data.pop('items')
            order = self.Meta.model.objects.create(customer=user, **validated_data)

            for order_item in order_items:
                _id = order_item.pop('item')
                try:
                    product = Product.objects.get(id=_id)
                    OrderItems.objects.create(order=order, customer=user, **order_item, product=product)
                except Product.DoesNotExist:
                    pass
            if order:
                message = f'Dear {order.customer.get_full_name()} , Your order of amount KES {order.get_total()} for ' \
                          f'order number {order.order_id} was placed successfully. Check your email for more ' \
                          f'order information.'
                send_sms_notification(message, order.customer.phone)
            return order

    def update(self, instance, validated_data):
        """Update the order and notify the customer via sms"""
        items = validated_data.pop('items')
        updated_field = [k for k in validated_data]
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save(update_fields=updated_field)

        """getting list of order items"""
        order_items = set(OrderItems.objects.filter(order=instance.id).values_list('id', flat=True))
        items_id = []
        for item in items:
            item_id = item.get('id')

            try:
                product_instance = Product.objects.get(id=item['item'])
            except Product.DoesNotExist:
                continue

            new_item = {
                'product': product_instance,
                'quantity': item.get('quantity'),
                'ordered': item.get('ordered'),
            }

            if item_id is not None and item_id in order_items:
                OrderItems.objects.filter(id=item_id).update(**new_item)
                items_id.append(item_id)
            else:
                OrderItems.objects.create(
                    order=instance,
                    customer=self.context['request'].user,
                    product=new_item['product'],
                    quantity=new_item['quantity'],
                    ordered=new_item['ordered']
                )

                items_id.append(item_id)

                for item_id in order_items:
                    if item_id not in items_id:
                        OrderItems.objects.filter(id=item_id).delete()
        message = f'Dear {instance.customer.get_full_name()} , Your order of amount KES {instance.get_total()} for ' \
                  f'order number {instance.order_id} has been updated successfully. Check your email for more ' \
                  f'order information.'
        send_sms_notification(message, instance.customer.phone)

        return instance
