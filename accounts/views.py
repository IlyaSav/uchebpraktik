from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, BeetleForm, ServiceForm, ArticleForm
from .models import Beetle, Service

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

from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render

def home(request):
    beetles = Beetle.objects.all()
    offers = Service.objects.order_by('price_min')[:3]
    return render(request, 'accounts/index.html', {'beetles': beetles, 'offers': offers})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

from .models import Service

def services(request):
    services = Service.objects.all()
    return render(request, 'accounts/services.html', {'services': services})

from django.shortcuts import get_object_or_404

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'accounts/service_detail.html', {'service': service})

def about(request):
    return render(request, 'accounts/about.html')

def order(request):
    return render(request, 'accounts/order.html')

def contacts(request):
    return render(request, 'accounts/contacts.html')

from .models import Article

def articles(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'accounts/articles.html', {'articles': articles})

def reviews(request):
    return render(request, 'accounts/reviews.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    beetle_form = BeetleForm()
    service_form = ServiceForm()
    article_form = ArticleForm()
    message = ''
    if request.method == 'POST':
        # Add new beetle
        if 'beetle_submit' in request.POST:
            beetle_form = BeetleForm(request.POST, request.FILES)
            if beetle_form.is_valid():
                beetle_form.save()
                beetle_form = BeetleForm()
        # Edit beetle
        elif 'beetle_edit' in request.POST:
            beetle_id = request.POST.get('beetle_id')
            beetle = Beetle.objects.get(id=beetle_id)
            beetle_form = BeetleForm(request.POST, request.FILES, instance=beetle)
            if beetle_form.is_valid():
                beetle_form.save()
                beetle_form = BeetleForm()
        # Delete beetle
        elif 'beetle_delete' in request.POST:
            beetle_id = request.POST.get('beetle_id')
            beetle = Beetle.objects.get(id=beetle_id)
            beetle.delete()
            beetle_form = BeetleForm()
        # Add new service
        elif 'service_submit' in request.POST:
            service_form = ServiceForm(request.POST, request.FILES)
            if service_form.is_valid():
                service_form.save()
                service_form = ServiceForm()
        # Edit service
        elif 'service_edit' in request.POST:
            service_id = request.POST.get('service_id')
            service = Service.objects.get(id=service_id)
            service_form = ServiceForm(request.POST, request.FILES, instance=service)
            if service_form.is_valid():
                service_form.save()
                service_form = ServiceForm()
        # Delete service
        elif 'service_delete' in request.POST:
            service_id = request.POST.get('service_id')
            service = Service.objects.get(id=service_id)
            service.delete()
            service_form = ServiceForm()
        # Add new article
        elif 'article_submit' in request.POST:
            article_form = ArticleForm(request.POST)
            if article_form.is_valid():
                article_form.save()
                article_form = ArticleForm()
        # Edit article
        elif 'article_edit' in request.POST:
            article_id = request.POST.get('article_id')
            article = Article.objects.get(id=article_id)
            article_form = ArticleForm(request.POST, instance=article)
            if article_form.is_valid():
                article_form.save()
                article_form = ArticleForm()
        # Delete article
        elif 'article_delete' in request.POST:
            article_id = request.POST.get('article_id')
            article = Article.objects.get(id=article_id)
            article.delete()
            article_form = ArticleForm()
    beetles = Beetle.objects.all()
    services = Service.objects.all()
    articles = Article.objects.all()
    return render(request, 'accounts/admin_panel.html', {
        'beetle_form': beetle_form,
        'service_form': service_form,
        'article_form': article_form,
        'message': message,
        'beetles': beetles,
        'services': services,
        'articles': articles,
    })
