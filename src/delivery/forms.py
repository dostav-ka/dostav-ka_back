from django import forms

from user.models import Courier


class AssignCourierForm(forms.Form):
    courier = forms.ModelChoiceField(queryset=Courier.objects.all(), label="Выберите курьера")