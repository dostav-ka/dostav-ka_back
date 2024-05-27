from django.urls import path

from .views import (
    ManagerRegistrationView, PersonalAccountView, ManagerLoginView,
    ManagerCreateView, ManagerView,
    CourierCreateView, CourierView, CourierConfirmTGView, CourierOrdersView, CourierListView
)

urlpatterns = [
    path('', PersonalAccountView.as_view(), name='personal'),
    path('registration', ManagerRegistrationView.as_view(), name='registration'),
    path('login', ManagerLoginView.as_view(), name='login'),
    path('manager/create', ManagerCreateView.as_view(), name='create_manager'),
    path('manager/<int:id>', ManagerView.as_view(), name='manager'),
    path('courier', CourierListView.as_view(), name='courier-list'),
    path('courier/create', CourierCreateView.as_view(), name='create_courier'),
    path('courier/<int:id>', CourierView.as_view(), name='courier'),
    path('courier/<int:id>/confirm', CourierConfirmTGView.as_view(), name='courier_confirm_tg'),
    path('courier/orders', CourierOrdersView.as_view(), name='courier_orders'),
]
