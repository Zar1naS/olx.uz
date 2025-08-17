from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from PIL import Image
import os

User = get_user_model()


class Category(models.Model):
    """Ad categories"""
    
    name = models.CharField(_('Nomi'), max_length=100)
    name_ru = models.CharField(_('Nomi (rus)'), max_length=100, blank=True)
    slug = models.SlugField(_('Slug'), unique=True)
    icon = models.CharField(_('Ikonka'), max_length=50, default='fas fa-tag')
    description = models.TextField(_('Tavsif'), blank=True)
    is_active = models.BooleanField(_('Faol'), default=True)
    order = models.PositiveIntegerField(_('Tartib'), default=0)
    created_at = models.DateTimeField(_('Yaratilgan sana'), auto_now_add=True)

    class Meta:
        verbose_name = _('Kategoriya')
        verbose_name_plural = _('Kategoriyalar')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ads:category', kwargs={'slug': self.slug})

    @property
    def ads_count(self):
        return self.ads.filter(is_active=True).count()


class Location(models.Model):
    """Locations for ads"""
    
    name = models.CharField(_('Nomi'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    is_active = models.BooleanField(_('Faol'), default=True)
    order = models.PositiveIntegerField(_('Tartib'), default=0)

    class Meta:
        verbose_name = _('Joylashuv')
        verbose_name_plural = _('Joylashuvlar')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def ads_count(self):
        return self.ads.filter(is_active=True).count()


class Ad(models.Model):
    """Main ad model"""
    
    STATUS_CHOICES = [
        ('active', _('Faol')),
        ('sold', _('Sotildi')),
        ('expired', _('Muddati tugagan')),
    ]

    CONDITION_CHOICES = [
        ('new', _('Yangi')),
        ('excellent', _('Zo\'r holatda')),
        ('good', _('Yaxshi holatda')),
        ('fair', _('Qoniqarli holatda')),
        ('poor', _('Yomon holatda')),
    ]

    title = models.CharField(_('Sarlavha'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True, blank=True)
    description = models.TextField(_('Tavsif'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads', verbose_name=_('Kategoriya'))
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='ads', verbose_name=_('Joylashuv'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads', verbose_name=_('Foydalanuvchi'))
    
    price = models.DecimalField(_('Narx'), max_digits=12, decimal_places=2)
    condition = models.CharField(_('Holati'), max_length=20, choices=CONDITION_CHOICES, default='good')
    
    phone = models.CharField(_('Telefon'), max_length=15)
    is_negotiable = models.BooleanField(_('Kelishish mumkin'), default=True)
    
    # Status fields
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(_('Faol'), default=True)
    is_featured = models.BooleanField(_('Tanlangan'), default=False)
    is_vip = models.BooleanField(_('VIP'), default=False)
    
    # Statistics
    views_count = models.PositiveIntegerField(_('Ko\'rishlar soni'), default=0)
    favorites_count = models.PositiveIntegerField(_('Tanlanganlar soni'), default=0)
    
    # Dates
    created_at = models.DateTimeField(_('Yaratilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Yangilangan sana'), auto_now=True)
    expires_at = models.DateTimeField(_('Tugash sanasi'), null=True, blank=True)
    
    # Many-to-many fields
    favorited_by = models.ManyToManyField(User, related_name='favorites', blank=True, verbose_name=_('Tanlanganlar'))

    class Meta:
        verbose_name = _('E\'lon')
        verbose_name_plural = _('E\'lonlar')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'location', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured', 'is_vip']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Ad.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ads:detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """Increment views count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def toggle_favorite(self, user):
        """Toggle favorite status for user"""
        if user in self.favorited_by.all():
            self.favorited_by.remove(user)
            self.favorites_count = max(0, self.favorites_count - 1)
            is_favorite = False
        else:
            self.favorited_by.add(user)
            self.favorites_count += 1
            is_favorite = True
        
        self.save(update_fields=['favorites_count'])
        return is_favorite

    @property
    def main_image(self):
        """Get main image"""
        return self.images.filter(is_main=True).first() or self.images.first()

    @property
    def is_owner(self):
        """Check if current user is owner"""
        # This will be set in views when needed
        return getattr(self, '_is_owner', False)


class AdImage(models.Model):
    """Ad images"""
    
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images', verbose_name=_('E\'lon'))
    image = models.ImageField(_('Rasm'), upload_to='ads/%Y/%m/%d/')
    is_main = models.BooleanField(_('Asosiy rasm'), default=False)
    order = models.PositiveIntegerField(_('Tartib'), default=0)
    created_at = models.DateTimeField(_('Yaratilgan sana'), auto_now_add=True)

    class Meta:
        verbose_name = _('E\'lon rasmi')
        verbose_name_plural = _('E\'lon rasmlari')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'{self.ad.title} - {self.order}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def delete(self, *args, **kwargs):
        # Delete image file when model is deleted
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class AdReport(models.Model):
    """Ad reports for inappropriate content"""
    
    REASON_CHOICES = [
        ('spam', _('Spam')),
        ('inappropriate', _('Nomaqbul kontent')),
        ('fraud', _('Firibgarlik')),
        ('duplicate', _('Takroriy e\'lon')),
        ('wrong_category', _('Noto\'g\'ri kategoriya')),
        ('other', _('Boshqa')),
    ]

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reports', verbose_name=_('E\'lon'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Foydalanuvchi'))
    reason = models.CharField(_('Sabab'), max_length=20, choices=REASON_CHOICES)
    description = models.TextField(_('Tavsif'), blank=True)
    created_at = models.DateTimeField(_('Yaratilgan sana'), auto_now_add=True)
    is_resolved = models.BooleanField(_('Hal qilingan'), default=False)

    class Meta:
        verbose_name = _('E\'lon shikoyati')
        verbose_name_plural = _('E\'lon shikoyatlari')
        unique_together = ['ad', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.ad.title} - {self.get_reason_display()}'
