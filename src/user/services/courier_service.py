from dataclasses import dataclass

from ..models import User, Courier


@dataclass
class CourierDataClass:
    email: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str


class CourierService:
    @staticmethod
    def create(courier_data: CourierDataClass):
        user = User.objects.create_mock_user(email=courier_data.email)
        manager = Courier.objects.create(
            user=user, phone=courier_data.phone,
            first_name=courier_data.first_name, last_name=courier_data.last_name,
            middle_name=courier_data.middle_name
        )
        return manager


class CourierCreateMediator:
    @staticmethod
    def execute(request, form):
        courier_data = CourierDataClass(
            form.get('email'), form.get('first_name'), form.get('last_name'),
            form.get('middle_name'), form.get('phone')
        )
        return CourierService.create(courier_data)
