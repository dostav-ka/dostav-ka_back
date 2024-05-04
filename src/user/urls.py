from django.urls import path

from .views import ManagerRegistrationView, PersonalAccountView

urlpatterns = [
    path('', PersonalAccountView.as_view(), name='personal'),
    path('registration', ManagerRegistrationView.as_view(), name='registration')
]
