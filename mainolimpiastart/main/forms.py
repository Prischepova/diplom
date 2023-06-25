from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import *

from typing import Iterable, NoReturn

# from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from django import forms
from django_filters import DateFilter, FilterSet
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """

    class Meta:
        model = Profile
        fields = ('slug', 'photo', 'phone')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class IndivUserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class IndivUpdateForm(forms.ModelForm):
    """
    Форма обновления данных документа пользователя
    """

    class Meta:
        model = Indiv
        fields = ('tutor', 'child_name', 'datetime', 'location_name',)

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class DocumentsUpdateForm(forms.ModelForm):
    """
    Форма обновления данных документа пользователя
    """

    class Meta:
        model = Documents
        fields = ('files',)

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class EventFilter(FilterSet):  # type: ignore
    start_date__gt = DateFilter(
        field_name="date_training",
        widget=DatePickerInput(),
    )

    class Meta:
        model = Schedule
        fields: Iterable[str] = []
