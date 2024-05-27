from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Order, Product, Address, Business
from .serializers import OrderSerializer, ProductSerializer, AddressSerializer, ClientSerializer, OrderStatusSerializer
from user.models import Client
from user.services.manager_service import ManagerService


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


class OrderStatusView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['id']
        order = get_object_or_404(Order, id=order_id)
        if order.status in [Order.Status.closed, Order.Status.completed]:
            return Response("Already ended", status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tg_id = serializer.validated_data['tg_id']
        order_status = serializer.validated_data['status']
        if order_status not in [Order.Status.completed, Order.Status.approved, Order.Status.closed]:
            return Response("Invalid status", status=status.HTTP_400_BAD_REQUEST)

        if not order.courier or order.courier.telegram_id != tg_id:
            return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)

        order.status = order_status
        order.save(update_fields=['status'])

        return Response("OK", status=status.HTTP_200_OK)


class OrderView(TemplateView):
    template_name = 'order/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['id']
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        context['couriers'] = ManagerService(self.request.user.manager).get_couriers()
        return context


class OrderListView(TemplateView):
    template_name = 'order/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = ManagerService(self.request.user.manager).get_orders()
        return context
