from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import ManagerRegistrationForm, ManagerLoginForm, CourierCreateForm
from .models import Courier, Manager
from .serializers import CourierTGSerializer
from .services.courier_service import CourierCreateMediator, CourierService
from .services.manager_service import ManagerRegistrationMediator, ManagerCreateMediator, ManagerService
from delivery.serializers import OrderSerializer


class ManagerRegistrationView(TemplateView):
    template_name = 'user/manager/registration.html'
    form_class = ManagerRegistrationForm
    success_url = reverse_lazy('user:personal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            manager = ManagerRegistrationMediator.execute(request, form.cleaned_data)
            login(request, manager.user)
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form_errors=form.errors))


class ManagerLoginView(TemplateView):
    template_name = 'user/manager/login.html'
    form_class = ManagerLoginForm
    success_url = reverse_lazy('user:personal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            else:
                form.add_error(None, 'Некорректный пароль.')

        return self.render_to_response(self.get_context_data(form_errors=form.errors))


class ManagerCreateView(TemplateView):
    template_name = 'user/manager/create.html'
    form_class = ManagerRegistrationForm
    success_url = reverse_lazy('user:personal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            manager = ManagerCreateMediator.execute(request, form.cleaned_data)
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form_errors=form.errors))


class CourierCreateView(TemplateView):
    template_name = 'user/courier/create.html'
    form_class = CourierCreateForm
    success_url = reverse_lazy('user:personal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            courier = CourierCreateMediator.execute(request, form.cleaned_data)
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form_errors=form.errors))


class PersonalAccountView(TemplateView):
    template_name = 'user/manager/personal_account.html'


class CourierView(TemplateView):
    template_name = 'user/courier/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courier_id = self.kwargs['id']
        courier = get_object_or_404(Courier, id=courier_id)
        context['courier'] = courier
        context['orders'] = CourierService(courier).get_orders()
        return context


class CourierListView(TemplateView):
    template_name = 'user/courier/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['couriers'] = ManagerService(self.request.user.manager).get_couriers()
        return context


class ManagerView(TemplateView):
    template_name = 'user/manager/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager_id = self.kwargs['id']
        manager = get_object_or_404(Manager, id=manager_id)
        context['manager'] = manager
        return context


class CourierConfirmTGView(APIView):
    def post(self, request, *args, **kwargs):
        courier_id = self.kwargs['id']
        courier = get_object_or_404(Courier, id=courier_id)
        if courier.telegram_id:
            return Response("Already confirmed", status=status.HTTP_400_BAD_REQUEST)

        serializer = CourierTGSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tg_id = serializer.validated_data['tg_id']
        courier.telegram_id = tg_id
        courier.save(update_fields=['telegram_id'])

        return Response("OK", status=status.HTTP_200_OK)


class CourierOrdersView(APIView):
    def get(self, request, *args, **kwargs):
        tg_id = request.query_params.get('tg_id')
        if tg_id is None:
            return Response({"detail": "tg_id parameter is required."}, status=400)

        courier = get_object_or_404(Courier, telegram_id=tg_id)
        orders = CourierService(courier).get_orders()
        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)
