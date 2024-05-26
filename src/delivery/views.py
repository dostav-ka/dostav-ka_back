from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Order, Product, Address, Business
from .serializers import OrderSerializer, ProductSerializer, AddressSerializer, ClientSerializer
from user.models import Client


class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('X-dostav-ka', None)
        if not token:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

        business = Business.objects.filter(token=token).first()
        if not business:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

        order_serializer = OrderSerializer(data=request.data)

        if not order_serializer.is_valid():
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_data = order_serializer.validated_data.pop('product')
        address_data = order_serializer.validated_data.pop('address')
        client_data = order_serializer.validated_data.pop('client')

        product_serializer = ProductSerializer(data=product_data)
        address_serializer = AddressSerializer(data=address_data)
        client_serializer = ClientSerializer(data=client_data)

        if not (product_serializer.is_valid() and address_serializer.is_valid() and client_serializer.is_valid()):
            raise ValidationError({
                'product': product_serializer.errors,
                'address': address_serializer.errors,
                'client': client_serializer.errors
            })

        product = Product.objects.create(**product_serializer.validated_data)
        address = Address.objects.create(**address_serializer.validated_data)
        client = Client.objects.create(**client_serializer.validated_data)

        order = Order.objects.create(
            product=product,
            address=address,
            client=client,
            expected_delivery_time=order_serializer.validated_data['expected_delivery_time'],
            payment_upon_receipt=order_serializer.validated_data['payment_upon_receipt'],
            delivery_cost=order_serializer.validated_data['delivery_cost'],
            total_cost=order_serializer.validated_data['total_cost'],
            business=business
        )

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
