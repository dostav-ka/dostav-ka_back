from rest_framework import serializers

from .models import Order, Product, Address
from user.models import Client


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'cost')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'house', 'housing', 'apartment', 'region', 'link']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'contact']


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    address = AddressSerializer()
    client = ClientSerializer()
    tg_id = serializers.CharField(source='courier.telegram_id')

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'address', 'client', 'expected_delivery_time',
            'payment_upon_receipt', 'delivery_cost', 'total_cost', 'tg_id'
        ]
        read_only_fields = ['id', 'tg_id']


class OrderStatusSerializer(serializers.Serializer):
    tg_id = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
