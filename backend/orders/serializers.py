from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Flower
from users.serializers import UserSerializer
from products.serializers import FlowerSerializer
import decimal
from rest_framework.exceptions import ValidationError

class OrderItemSerializer(serializers.ModelSerializer):
    flower = FlowerSerializer(read_only=True)
    flower_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'flower', 'flower_id', 'quantity', 'price')

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'created_at', 'updated_at', 'total_price', 'status', 'shipping_address', 
                 'order_type', 'booking_date', 'delivery_date', 'special_requirements', 
                 'recipient_name', 'recipient_phone', 'items')
        extra_kwargs = {
            'total_price': {'read_only': True}
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = validated_data.pop('user')

        total_price = sum(decimal.Decimal(item_data['price']) * item_data['quantity'] for item_data in items_data)

        if user.balance < total_price:
            raise ValidationError('余额不足，无法完成支付。')

        order = Order.objects.create(user=user, total_price=total_price, status='processing', **validated_data)
        
        user.balance -= total_price
        user.save()

        for item_data in items_data:
            flower = Flower.objects.get(id=item_data['flower_id'])
            OrderItem.objects.create(order=order, flower=flower, quantity=item_data['quantity'], price=item_data['price'])
            
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance