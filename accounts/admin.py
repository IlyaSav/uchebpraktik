from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Beetle, Service, Article
from .models import SiteSettings

# Unregister the original User admin
admin.site.unregister(User)

# Register Beetle model
@admin.register(Beetle)
class BeetleAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')

    def image_tag(self, obj):
        if obj.beetle_image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.beetle_image.url)
        return "-"
    image_tag.short_description = 'Изображение'

# Register Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_min', 'price_max')
    list_filter = ('price_min', 'price_max')
    search_fields = ('name', 'description')

# Register Article model
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'recommendations')
    list_filter = ('created_at', 'updated_at')

# Extend UserAdmin to show groups in list display and filter
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_groups')
    list_filter = ('is_staff', 'is_active', 'groups')
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Роли'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
