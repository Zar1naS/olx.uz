#!/usr/bin/env python
"""
Bu skript yaratilgan namunaviy ma'lumotlarni ko'rsatadi.
Ishga tushirish: python show_sample_data.py
"""

import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ads.models import Category, Location, Ad, AdImage

def show_sample_data():
    print("🛒 OLX NAMUNAVIY MA'LUMOTLAR BAZASI")
    print("=" * 50)
    
    print(f"\n📱 KATEGORIYALAR ({Category.objects.count()} ta):")
    for category in Category.objects.all():
        ads_count = category.ads.count()
        print(f"   {category.icon} {category.name} ({ads_count} ta e'lon)")
    
    print(f"\n📍 JOYLASHUVLAR ({Location.objects.count()} ta):")
    for location in Location.objects.all():
        ads_count = location.ads.count()
        print(f"   📌 {location.name} ({ads_count} ta e'lon)")
    
    print(f"\n📢 E'LONLAR ({Ad.objects.count()} ta):")
    print("\nBa'zi mashhur e'lonlar:")
    
    # Ko'p ko'rilgan e'lonlar
    popular_ads = Ad.objects.order_by('-views_count')[:5]
    for ad in popular_ads:
        main_image = "🖼️" if ad.images.exists() else "❌"
        print(f"   {main_image} {ad.title}")
        print(f"      💰 {ad.price:,} so'm | 👀 {ad.views_count} marta ko'rildi")
        print(f"      📍 {ad.location.name} | 📱 {ad.category.name}")
        print(f"      📝 {ad.description[:60]}...")
        print()
    
    print(f"\n🖼️ RASMLAR ({AdImage.objects.count()} ta):")
    with_images = Ad.objects.filter(images__isnull=False).count()
    without_images = Ad.objects.filter(images__isnull=True).count()
    print(f"   ✅ Rasmi bor: {with_images} ta e'lon")
    print(f"   ❌ Rasmsiz: {without_images} ta e'lon")
    
    print(f"\n💎 MAXSUS E'LONLAR:")
    featured_count = Ad.objects.filter(is_featured=True).count()
    vip_count = Ad.objects.filter(is_vip=True).count()
    print(f"   ⭐ Tanlangan e'lonlar: {featured_count} ta")
    print(f"   💎 VIP e'lonlar: {vip_count} ta")
    
    print("\n" + "=" * 50)
    print("🎉 Namunaviy ma'lumotlar muvaffaqiyatli yaratildi!")
    print("Django admin panel orqali ko'rishingiz mumkin: /admin/")

if __name__ == "__main__":
    show_sample_data()
