# Generated by Django 5.0.2 on 2024-05-26 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('house', models.CharField(max_length=100)),
                ('housing', models.CharField(max_length=100)),
                ('apartment', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('lenght', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('widht', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='business',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business', to='delivery.address'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_delivery_time', models.DateTimeField(blank=True, null=True)),
                ('actual_delivery_time', models.DateTimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('creating', 'Creating'), ('approved', 'Approved'), ('completed', 'Сompleted'), ('closed', 'Closed')], default='creating', max_length=50)),
                ('payment_upon_receipt', models.BooleanField(default=False)),
                ('delivery_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='delivery.address')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='delivery.business')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user.client')),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='user.courier')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='delivery.product')),
            ],
        ),
    ]