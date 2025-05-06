from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=EmailAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('about/', views.about, name='about'),
    path('order/', views.order, name='order'),
    path('contacts/', views.contacts, name='contacts'),
    path('articles/', views.articles, name='articles'),
    path('reviews/', views.reviews, name='reviews'),
]
