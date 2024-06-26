from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from .forms import ManagerRegistrationForm, ManagerLoginForm, CourierCreateForm
from .models import Courier
from .services.courier_service import CourierCreateMediator
from .services.manager_service import ManagerRegistrationMediator, ManagerCreateMediator


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
            print(user)
            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            else:
                form.add_error(None, 'Некорректный пароль.')
            print(form.errors)

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
        return context
