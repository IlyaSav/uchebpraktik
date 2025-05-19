from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Beetle, Service, Article, ServiceRequest, Review, NewsletterSubscription, News

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

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок новости'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Содержание новости'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['service', 'name', 'text']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв', 'rows': 4}),
        }
        labels = {
            'service': 'Услуга (необязательно)',
            'name': 'Ваше имя',
            'text': 'Текст отзыва',
        }

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш email',
                'required': 'required'
            })
        }
        labels = {
            'email': 'Электронная почта'
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }