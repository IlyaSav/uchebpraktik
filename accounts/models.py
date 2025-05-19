from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import uuid

class Beetle(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True, null=True, help_text="CSS class for the beetle icon, e.g. 'fas fa-bug'")
    beetle_image = models.ImageField(upload_to='beetle_images/', blank=True, null=True, help_text="Image of the beetle")
    description = models.TextField(help_text="Solution for getting rid of this beetle at home")

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Минимальная цена", default=0.00)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Максимальная цена", default=0.00)
    equipment_image = models.ImageField(upload_to='equipment/', blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    recommendations = models.TextField(verbose_name="Рекомендации по профилактике и санитарии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class RequestStatus(models.TextChoices):
    NEW = 'new', 'Новая'
    VIEWED = 'viewed', 'Просмотрено'
    IN_PROGRESS = 'in_progress', 'В обработке'
    COMPLETED = 'completed', 'Услуга оказана'
    CANCELLED = 'cancelled', 'Отменена'

class ServiceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True)
    custom_service = models.CharField(max_length=200, blank=True, null=True)
    problem_description = models.TextField()
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=RequestStatus.choices, default=RequestStatus.NEW)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заявка #{self.id} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if self.service and not self.price:
            self.price = self.service.price_min
        super().save(*args, **kwargs)

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100, verbose_name="Имя")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв от {self.name} ({self.created_at.strftime('%d.%m.%Y')})"

class SiteSettings(models.Model):
    phone_number = models.CharField(max_length=20, verbose_name="Телефон для связи")
    
    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Настройки сайта"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждена")
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Токен подтверждения")
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписка на новости"
        verbose_name_plural = "Подписки на новости"