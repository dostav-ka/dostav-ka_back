from dataclasses import dataclass

from ..models import User, Courier
from delivery.models import Business, Order


@dataclass
class CourierDataClass:
    email: str
    first_name: str
    last_name: str
    middle_name: str
    phone: str
    business: Business


class CourierService:
    def __init__(self, courier):
        self.courier = courier

    def get_orders(self):
        return Order.objects.filter(courier=self.courier).order_by('-created_date')[:5]

    @staticmethod
    def create(courier_data: CourierDataClass):
        user = User.objects.create_mock_user(email=courier_data.email)
        courier = Courier.objects.create(
            user=user, phone=courier_data.phone,
            first_name=courier_data.first_name, last_name=courier_data.last_name,
            middle_name=courier_data.middle_name, business=courier_data.business
        )
        return courier


class CourierCreateMediator:
    @staticmethod
    def execute(request, form):
        business = request.user.manager.business
        courier_data = CourierDataClass(
            form.get('email'), form.get('first_name'), form.get('last_name'),
            form.get('middle_name'), form.get('phone'), business
        )
        return CourierService.create(courier_data)
