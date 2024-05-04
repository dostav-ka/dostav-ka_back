from django.contrib.auth import login
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import ManagerRegistrationForm
from .services.manager_service import ManagerRegistrationMediator


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
            return self.render_to_response(self.get_context_data(form=form))


class PersonalAccountView(TemplateView):
    template_name = 'user/manager/personal_account.html'
