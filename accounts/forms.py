from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Beetle, Service, Article
from .models import ServiceRequest, Service

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

class BeetleForm(forms.ModelForm):
    class Meta:
        model = Beetle
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class ServiceRequestForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        label='Тип услуги',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'service-select'})
    )
    custom_service = forms.CharField(
        required=False,
        label='Другой тип проблемы',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    problem_description = forms.CharField(
        label='Описание проблемы',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    full_name = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'})
    )
    address = forms.CharField(
        label='Адрес',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    class Meta:
        model = ServiceRequest
        fields = ['service', 'custom_service', 'problem_description', 'full_name', 'phone', 'address']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('service') and not cleaned_data.get('custom_service'):
            raise forms.ValidationError("Укажите тип услуги или опишите проблему")
        return cleaned_data
