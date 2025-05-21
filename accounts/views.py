import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import UserRegisterForm, BeetleForm, ServiceForm, ArticleForm, ServiceRequestForm, ReviewForm, NewsletterSubscriptionForm, NewsForm, UserProfileForm
from .models import Beetle, Service, Article, ServiceRequest, RequestStatus, Review, SiteSettings, NewsletterSubscription, News
from django.db.models import Count

# Настройка логирования для диагностики ошибок
logger = logging.getLogger(__name__)

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

def home(request):
    beetles = Beetle.objects.all()
    offers = Service.objects.order_by('price_min')[:3]
    return render(request, 'accounts/index.html', {'beetles': beetles, 'offers': offers})

@login_required
def profile(request):
    user_requests = ServiceRequest.objects.filter(user=request.user).order_by('-created_at')
    profile_form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'user_requests': user_requests, 'profile_form': profile_form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            return render(request, 'accounts/profile.html', {
                'user_requests': ServiceRequest.objects.filter(user=request.user).order_by('-created_at'),
                'profile_form': form
            })
    return redirect('profile')

def services(request):
    services = Service.objects.all()
    return render(request, 'accounts/services.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'accounts/service_detail.html', {'service': service})

def about(request):
    return render(request, 'accounts/about.html')

def contacts(request):
    return render(request, 'accounts/contacts.html')

def order(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            return redirect('profile')
    else:
        form = ServiceRequestForm()
    services = Service.objects.all()
    return render(request, 'accounts/order.html', {'form': form, 'services': services})

def get_service_price(request):
    if request.method == 'GET' and request.GET.get('service_id'):
        service_id = request.GET.get('service_id')
        try:
            service = Service.objects.get(id=service_id)
            return JsonResponse({'price': str(service.price_min)})
        except Service.DoesNotExist:
            return JsonResponse({'price': None})
    return JsonResponse({'price': None})

def articles(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'accounts/articles.html', {'articles': articles})

def reviews(request):
    services = Service.objects.all()
    reviews_list = Review.objects.order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
                if not review.name:
                    review.name = request.user.username
            review.save()
            return redirect('reviews')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name() or request.user.username
        form = ReviewForm(initial=initial)
    return render(request, 'accounts/reviews.html', {'reviews': reviews_list, 'form': form, 'services': services})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    beetle_form = BeetleForm()
    service_form = ServiceForm()
    article_form = ArticleForm()
    news_form = NewsForm()
    message = ''
    if request.method == 'POST':
        if 'beetle_submit' in request.POST:
            beetle_form = BeetleForm(request.POST, request.FILES)
            if beetle_form.is_valid():
                beetle_form.save()
                message = 'Вредитель успешно добавлен!'
                beetle_form = BeetleForm()
        elif 'beetle_edit' in request.POST:
            beetle_id = request.POST.get('beetle_id')
            beetle = Beetle.objects.get(id=beetle_id)
            beetle_form = BeetleForm(request.POST, request.FILES, instance=beetle)
            if beetle_form.is_valid():
                beetle_form.save()
                message = 'Вредитель успешно обновлен!'
                beetle_form = BeetleForm()
        elif 'beetle_delete' in request.POST:
            beetle_id = request.POST.get('beetle_id')
            beetle = Beetle.objects.get(id=beetle_id)
            beetle.delete()
            message = 'Вредитель успешно удален!'
            beetle_form = BeetleForm()
        elif 'service_submit' in request.POST:
            service_form = ServiceForm(request.POST, request.FILES)
            if service_form.is_valid():
                service_form.save()
                message = 'Услуга успешно добавлена!'
                service_form = ServiceForm()
        elif 'service_edit' in request.POST:
            service_id = request.POST.get('service_id')
            service = Service.objects.get(id=service_id)
            service_form = ServiceForm(request.POST, request.FILES, instance=service)
            if service_form.is_valid():
                service_form.save()
                message = 'Услуга успешно обновлена!'
                service_form = ServiceForm()
        elif 'service_delete' in request.POST:
            service_id = request.POST.get('service_id')
            service = Service.objects.get(id=service_id)
            service.delete()
            message = 'Услуга успешно удалена!'
            service_form = ServiceForm()
        elif 'article_submit' in request.POST:
            article_form = ArticleForm(request.POST)
            if article_form.is_valid():
                article_form.save()
                message = 'Статья успешно добавлена!'
                article_form = ArticleForm()
        elif 'article_edit' in request.POST:
            article_id = request.POST.get('article_id')
            article = Article.objects.get(id=article_id)
            article_form = ArticleForm(request.POST, instance=article)
            if article_form.is_valid():
                article_form.save()
                message = 'Статья успешно обновлена!'
                article_form = ArticleForm()
        elif 'article_delete' in request.POST:
            article_id = request.POST.get('article_id')
            article = Article.objects.get(id=article_id)
            article.delete()
            message = 'Статья успешно удалена!'
            article_form = ArticleForm()
        elif 'news_submit' in request.POST:
            news_form = NewsForm(request.POST)
            if news_form.is_valid():
                news = news_form.save()
                message = 'Новость успешно добавлена и отправлена подтвержденным подписчикам!'
                news_form = NewsForm()
                subscribers = NewsletterSubscription.objects.filter(is_confirmed=True)
                email_messages = []
                subject = news.title
                message_body = f"Уважаемый подписчик,\n\n" \
                               f"Мы рады поделиться новой новостью:\n\n" \
                               f"{news.title}\n\n" \
                               f"{news.content}\n\n" \
                               f"С уважением,\nКоманда ЭкоСтандарт"
                from_email = settings.DEFAULT_FROM_EMAIL
                for subscriber in subscribers:
                    email_messages.append((subject, message_body, from_email, [subscriber.email]))
                try:
                    send_mass_mail(email_messages, fail_silently=False)
                except Exception as e:
                    message = f'Новость добавлена, но отправка писем не удалась: {str(e)}'
        elif 'news_edit' in request.POST:
            news_id = request.POST.get('news_id')
            news = News.objects.get(id=news_id)
            news_form = NewsForm(request.POST, instance=news)
            if news_form.is_valid():
                news_form.save()
                message = 'Новость успешно обновлена!'
                news_form = NewsForm()
        elif 'news_delete' in request.POST:
            news_id = request.POST.get('news_id')
            news = News.objects.get(id=news_id)
            news.delete()
            message = 'Новость успешно удалена!'
            news_form = NewsForm()
    beetles = Beetle.objects.all()
    services = Service.objects.all()
    articles = Article.objects.all()
    news = News.objects.all()
    return render(request, 'accounts/admin_panel.html', {
        'beetle_form': beetle_form,
        'service_form': service_form,
        'article_form': article_form,
        'news_form': news_form,
        'message': message,
        'beetles': beetles,
        'services': services,
        'articles': articles,
        'news': news,
    })

def is_admin_or_manager(user):
    return user.is_staff or user.groups.filter(name='Менеджер').exists()

@login_required
@user_passes_test(is_admin_or_manager)
def request_list(request):
    requests = ServiceRequest.objects.all().order_by('-created_at')
    status_choices = RequestStatus.choices
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        if request_id and new_status:
            service_request = ServiceRequest.objects.get(id=request_id)
            service_request.status = new_status
            service_request.save()
            return redirect('request_detail', pk=request_id)
    return render(request, 'accounts/request_list.html', {'requests': requests, 'status_choices': status_choices})

@login_required
@user_passes_test(is_admin_or_manager)
def request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    status_choices = RequestStatus.choices
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            service_request.status = new_status
            service_request.save()
            return redirect('request_detail', pk=pk)
    return render(request, 'accounts/request_detail.html', {'request': service_request, 'status_choices': status_choices})

def newsletter_subscribe(request):
    """
    Обработка подписки на рассылку.
    Проверяет существующие подписки, создаёт новые, отправляет письмо с подтверждением.
    Включает полную обработку исключений и логирование для диагностики ошибок.
    """
    logger.info("Начало обработки newsletter_subscribe")
    if request.method != 'POST':
        logger.info("Неверный метод запроса")
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса.'}, status=400)

    try:
        form = NewsletterSubscriptionForm(request.POST)
        email = request.POST.get('email', '').strip().lower()
        logger.info(f"POST data: {request.POST}, Email: {email}")

        # Проверка настроек
        if not hasattr(settings, 'BASE_URL'):
            logger.error("BASE_URL не определён в settings.py")
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка конфигурации сервера.'
            }, status=500)
        if not hasattr(settings, 'DEFAULT_FROM_EMAIL'):
            logger.error("DEFAULT_FROM_EMAIL не определён в settings.py")
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка конфигурации сервера.'
            }, status=500)

        # Проверка существующей подписки
        try:
            subscription = NewsletterSubscription.objects.get(email=email)
            logger.info(f"Найдена существующая подписка: {subscription}, Подтверждена: {subscription.is_confirmed}")
            if subscription.is_confirmed:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Этот email уже подписан и подтверждён.'
                })
        except NewsletterSubscription.DoesNotExist:
            logger.info("Подписка не найдена")
            if form.is_valid():
                try:
                    subscription = form.save()
                    logger.info(f"Новая подписка создана: {subscription}")
                except Exception as e:
                    logger.error(f"Ошибка при сохранении подписки: {str(e)}", exc_info=True)
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Ошибка при создании подписки.'
                    }, status=500)
            else:
                error_message = 'Пожалуйста, введите корректный email.'
                if 'email' in form.errors:
                    for error in form.errors['email']:
                        if error['code'] == 'invalid':
                            error_message = 'Пожалуйста, введите корректный email.'
                logger.info(f"Ошибка формы: {error_message}")
                return JsonResponse({
                    'status': 'error',
                    'message': error_message
                })

        # Формирование письма
        try:
            confirmation_url = f"{settings.BASE_URL}/accounts/confirm-subscription/{subscription.confirmation_token}/"
            logger.info(f"Confirmation URL: {confirmation_url}")
            subject = "Подтверждение подписки на новости"
            message = render_to_string('accounts/email_subscription_confirmation.html', {
                'confirmation_url': confirmation_url,
            })
            logger.info("Шаблон письма успешно отрендерен")
        except Exception as e:
            logger.error(f"Ошибка при рендеринге шаблона: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка при подготовке письма.'
            }, status=500)

        # Отправка письма
        try:
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message,
                fail_silently=False,
            )
            logger.info("Письмо успешно отправлено")
            return JsonResponse({
                'status': 'success',
                'message': 'Пожалуйста, подтвердите подписку, перейдя по ссылке, отправленной на ваш email.'
            })
        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка при отправке письма.'
            }, status=500)

    except Exception as e:
        logger.error(f"Необработанная ошибка в newsletter_subscribe: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Внутренняя ошибка сервера.'
        }, status=500)

def confirm_subscription(request, token):
    """
    Обработка подтверждения подписки.
    Показывает модальное окно с результатом подтверждения.
    """
    logger.info(f"Начало обработки confirm_subscription с токеном: {token}")
    try:
        subscription = NewsletterSubscription.objects.get(confirmation_token=token)
        if not subscription.is_confirmed:
            subscription.is_confirmed = True
            subscription.save()
            message = 'Ваша подписка успешно подтверждена! Вы будете получать наши новости.'
            status = 'success'
            logger.info(f"Подписка подтверждена для: {subscription.email}")
        else:
            message = 'Эта подписка уже подтверждена.'
            status = 'info'
            logger.info(f"Подписка уже подтверждена для: {subscription.email}")
    except NewsletterSubscription.DoesNotExist:
        message = 'Недействительный токен подтверждения.'
        status = 'error'
        logger.error(f"Недействительный токен: {token}")

    return render(request, 'accounts/index.html', {
        'confirmation_message': message,
        'confirmation_status': status,
        'beetles': Beetle.objects.all(),
        'offers': Service.objects.order_by('price_min')[:3]
    })

def get_global_context():
    return {
        'site_settings': SiteSettings.objects.first() or SiteSettings(phone_number="+79508102029")
    }

class GlobalContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_global_context())
        return context

@login_required
@user_passes_test(lambda u: u.is_staff)
def site_stats(request):
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    total_requests = ServiceRequest.objects.count()
    new_requests = ServiceRequest.objects.filter(status='new').count()
    in_progress_requests = ServiceRequest.objects.filter(status='in_progress').count()
    completed_requests = ServiceRequest.objects.filter(status='completed').count()
    cancelled_requests = ServiceRequest.objects.filter(status='cancelled').count()
    total_reviews = Review.objects.count()
    total_subscriptions = NewsletterSubscription.objects.count()
    confirmed_subscriptions = NewsletterSubscription.objects.filter(is_confirmed=True).count()
    total_services = Service.objects.count()
    total_articles = Article.objects.count()
    total_beetles = Beetle.objects.count()
    total_news = News.objects.count()
    top_services = Service.objects.annotate(
        request_count=Count('servicerequest')
    ).order_by('-request_count')[:5]

    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'total_requests': total_requests,
        'new_requests': new_requests,
        'in_progress_requests': in_progress_requests,
        'completed_requests': completed_requests,
        'cancelled_requests': cancelled_requests,
        'total_reviews': total_reviews,
        'total_subscriptions': total_subscriptions,
        'confirmed_subscriptions': confirmed_subscriptions,
        'total_services': total_services,
        'total_articles': total_articles,
        'total_beetles': total_beetles,
        'total_news': total_news,
        'top_services': top_services,
    }

    return render(request, 'accounts/stats.html', {'stats': stats})