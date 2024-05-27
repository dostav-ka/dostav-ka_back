from django.urls import path

from .views import OrderCreateView, OrderStatusView, OrderListView, OrderView

urlpatterns = [
    path('create', OrderCreateView.as_view(), name='api'),
    path('order', OrderListView.as_view(), name='order-list'),
    path('order/<int:id>', OrderView.as_view(), name='order'),
    path('order/<int:id>/status', OrderStatusView.as_view(), name='order_status'),
]
