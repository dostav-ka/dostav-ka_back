from django.urls import path

from .views import ManagerRegistrationView, PersonalAccountView, ManagerLoginView, ManagerCreateView, CourierCreateView

urlpatterns = [
    path('', PersonalAccountView.as_view(), name='personal'),
    path('registration', ManagerRegistrationView.as_view(), name='registration'),
    path('login', ManagerLoginView.as_view(), name='login'),
    path('manager/create', ManagerCreateView.as_view(), name='create_manager'),
    path('courier/create', CourierCreateView.as_view(), name='create_courier'),
]
