from django import forms

from .models import Manager, User


class ManagerRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()

    class Meta:
        model = Manager
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'phone', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Пользователь с таким email уже существует.")
        else:
            raise forms.ValidationError("Поле email обязательно для заполнения.")

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Пароли не совпадают.")
        else:
            raise forms.ValidationError("Поля пароля и подтверждения пароля обязательны для заполнения.")

        return cleaned_data

