from django.urls import path

from .views import OrderCreateView, OrderStatusView

urlpatterns = [
    path('create', OrderCreateView.as_view(), name='api'),
    path('order/<int:id>/status', OrderStatusView.as_view(), name='order_status'),
]
