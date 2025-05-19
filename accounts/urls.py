from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm
from .views import order, get_service_price

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=EmailAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('about/', views.about, name='about'),
    path('order/', views.order, name='order'),
    path('contacts/', views.contacts, name='contacts'),
    path('articles/', views.articles, name='articles'),
    path('reviews/', views.reviews, name='reviews'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('order/', order, name='order'),
    path('get-service-price/', get_service_price, name='get_service_price'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('confirm-subscription/<uuid:token>/', views.confirm_subscription, name='confirm_subscription'),
    path('stats/', views.site_stats, name='site_stats'),  # New stats URL
]