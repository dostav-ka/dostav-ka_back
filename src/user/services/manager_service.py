from dataclasses import dataclass

from ..models import User, Manager, Courier
from delivery.models import Business, Order


@dataclass
class ManagerDataClass:
    email: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str
    password: str
    business: Business


class ManagerService:
    def __init__(self, manager):
        self.manager = manager

    def get_orders(self):
        return Order.objects.filter(business=self.manager.business).order_by('-created_date')[:5]

    def get_couriers(self):
        return Courier.objects.filter(business=self.manager.business)

    def get_managers(self):
        return Manager.objects.filter(business=self.manager.business)

    @staticmethod
    def create(manager_data: ManagerDataClass):
        user = User.objects.create_user(email=manager_data.email, password=manager_data.password)
        manager = Manager.objects.create(
            user=user, phone=manager_data.phone,
            first_name=manager_data.first_name, last_name=manager_data.last_name,
            middle_name=manager_data.middle_name, business=manager_data.business
        )
        return manager


class ManagerRegistrationMediator:
    @staticmethod
    def execute(request, form):
        manager_data = ManagerDataClass(
            form.get('email'), form.get('first_name'), form.get('last_name'),
            form.get('middle_name'), form.get('phone'), form.get('password')
        )
        return ManagerService.create(manager_data)


class ManagerCreateMediator:
    @staticmethod
    def execute(request, form):
        business = request.user.manager.business
        manager_data = ManagerDataClass(
            form.get('email'), form.get('first_name'), form.get('last_name'),
            form.get('middle_name'), form.get('phone'), form.get('password'), business
        )
        return ManagerService.create(manager_data)
