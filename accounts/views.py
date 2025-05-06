from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Beetle

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

from django.shortcuts import render

def home(request):
    beetles = Beetle.objects.all()
    return render(request, 'accounts/index.html', {'beetles': beetles})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def services(request):
    return render(request, 'accounts/services.html')

def about(request):
    return render(request, 'accounts/about.html')

def order(request):
    return render(request, 'accounts/order.html')

def contacts(request):
    return render(request, 'accounts/contacts.html')

def articles(request):
    return render(request, 'accounts/articles.html')

def reviews(request):
    return render(request, 'accounts/reviews.html')
