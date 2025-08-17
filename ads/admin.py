from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Location, Ad, AdImage, AdReport


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'ads_count', 'is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'name_ru')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'ads_count', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1
    max_num = 10
    fields = ('image', 'is_main', 'order')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'user', 'price', 'status', 'is_active', 'is_featured', 'is_vip', 'views_count', 'created_at')
    list_filter = ('status', 'is_active', 'is_featured', 'is_vip', 'category', 'location', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'phone')
    readonly_fields = ('views_count', 'favorites_count', 'created_at', 'updated_at')
    list_editable = ('is_active', 'is_featured', 'is_vip')
    date_hierarchy = 'created_at'
    inlines = [AdImageInline]
    
    fieldsets = (
        (_('Asosiy ma\'lumotlar'), {
            'fields': ('title', 'description', 'category', 'location', 'user')
        }),
        (_('Narx va holat'), {
            'fields': ('price', 'condition', 'is_negotiable')
        }),
        (_('Aloqa'), {
            'fields': ('phone',)
        }),
        (_('Status'), {
            'fields': ('status', 'is_active', 'is_featured', 'is_vip')
        }),
        (_('Statistika'), {
            'fields': ('views_count', 'favorites_count'),
            'classes': ('collapse',)
        }),
        (_('Sanalar'), {
            'fields': ('created_at', 'updated_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'location', 'user')


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'is_main', 'order', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('ad__title',)
    list_editable = ('is_main', 'order')
    raw_id_fields = ('ad',)


@admin.register(AdReport)
class AdReportAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user', 'reason', 'created_at', 'is_resolved')
    list_filter = ('reason', 'is_resolved', 'created_at')
    search_fields = ('ad__title', 'user__username', 'description')
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('ad', 'user')
    
    fieldsets = (
        (_('Report ma\'lumotlari'), {
            'fields': ('ad', 'user', 'reason', 'description')
        }),
        (_('Status'), {
            'fields': ('is_resolved', 'created_at')
        }),
    )
