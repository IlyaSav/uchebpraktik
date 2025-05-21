from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Beetle, Service, Article, ServiceRequest, Review, NewsletterSubscription, News

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

    def clean_username(self):
        return self.cleaned_data['username'].strip().lower()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BeetleForm(forms.ModelForm):
    class Meta:
        model = Beetle
        fields = ['name', 'icon_class', 'beetle_image', 'description']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price_min', 'price_max', 'equipment_image']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'recommendations']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service', 'custom_service', 'problem_description', 'full_name', 'phone', 'address']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['service', 'name', 'text']

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']