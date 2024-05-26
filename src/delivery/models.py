from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    address = models.OneToOneField(
        'Address', on_delete=models.CASCADE, related_name='business', null=True, blank=True
    )

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    lenght = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    widht = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    class Status(models.TextChoices):
        creating = 'creating', 'Creating'
        approved = 'approved', 'Approved'
        completed = 'completed', 'Сompleted'
        closed = 'closed', 'Closed'

    product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, related_name='orders', null=True, blank=True
    )
    client = models.ForeignKey(
        'user.Client', on_delete=models.SET_NULL, related_name='orders', null=True, blank=True
    )
    courier = models.ForeignKey(
        'user.Courier', on_delete=models.SET_NULL, related_name='orders', null=True, blank=True
    )
    expected_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.creating)
    address = models.ForeignKey(
        'Address', on_delete=models.CASCADE, related_name='orders'
    )
    business = models.ForeignKey(
        'Business', on_delete=models.CASCADE, related_name='orders'
    )
    payment_upon_receipt = models.BooleanField(default=False)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    housing = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    link = models.CharField(max_length=256)
