from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profil ma\'lumotlari')
    fk_name = 'user'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom user admin - foydalanuvchi qo'shish taqiqlangan"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'location', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    # Allow superusers to add users through admin
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            # Regular staff users cannot see/edit admin permissions
            return (
                (None, {'fields': ('username',)}),
                (_('Shaxsiy ma\'lumotlar'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'location', 'birth_date')}),
                (_('Status'), {'fields': ('is_active', 'is_verified')}),
                (_('Muhim sanalar'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
            )
        # Superusers see all fields
        return (
            (None, {'fields': ('username', 'password')}),
            (_('Shaxsiy ma\'lumotlar'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'location', 'birth_date')}),
            (_('Ruxsatlar'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
            (_('Muhim sanalar'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
        )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    inlines = [UserProfileInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin - foydalanuvchi qo'shish taqiqlangan"""
    
    list_display = ('user', 'show_phone', 'show_email', 'website')
    list_filter = ('show_phone', 'show_email')
    search_fields = ('user__username', 'user__email', 'bio', 'website')
    raw_id_fields = ('user',)
    
    fieldsets = (
        (_('Asosiy ma\'lumotlar'), {'fields': ('user', 'bio')}),
        (_('Ijtimoiy tarmoqlar'), {'fields': ('website', 'facebook', 'instagram', 'telegram')}),
        (_('Maxfiylik sozlamalari'), {'fields': ('show_phone', 'show_email')}),
    )
    
    # Admin orqali profil qo'shishni taqiqlash
    def has_add_permission(self, request):
        return False  # Admin panel orqali profil qo'shish mumkin emas
