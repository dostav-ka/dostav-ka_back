from dataclasses import dataclass

from ..models import User, Manager


@dataclass
class ManagerDataClass:
    email: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str
    password: str


class ManagerService:
    @staticmethod
    def create(manager_data: ManagerDataClass):
        user = User.objects.create_user(email=manager_data.email, password=manager_data.password)
        manager = Manager.objects.create(
            user=user, phone=manager_data.phone,
            first_name=manager_data.first_name, last_name=manager_data.last_name,
            middle_name=manager_data.middle_name
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
