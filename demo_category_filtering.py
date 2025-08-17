#!/usr/bin/env python
"""
Bu script kategoriya sahifasidagi filterlash funksiyalarini namoyish etadi.
"""

import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ads.models import Category, Location, Ad
from django.db.models import Q

def demo_category_filtering():
    print("🔍 KATEGORIYA SAHIFASI FILTERLASH DEMO")
    print("=" * 50)
    
    # Get a category with many ads
    category = Category.objects.get(name='Elektron texnikalar')
    
    print(f"📱 Kategoriya: {category.name}")
    print(f"📢 Jami e'lonlar: {category.ads.count()} ta")
    print()
    
    # Test location filtering
    print("📍 JOYLASHUV BO'YICHA FILTERLASH:")
    locations = Location.objects.all()[:5]  # First 5 locations
    
    for location in locations:
        count = category.ads.filter(location=location).count()
        print(f"   {location.name}: {count} ta e'lon")
    print()
    
    # Test price filtering
    print("💰 NARX BO'YICHA FILTERLASH:")
    total_ads = category.ads.count()
    
    # Price ranges
    ranges = [
        (0, 1000000, "1 mln so'mgacha"),
        (1000000, 5000000, "1-5 mln so'm"),
        (5000000, 10000000, "5-10 mln so'm"),
        (10000000, float('inf'), "10 mln so'mdan yuqori")
    ]
    
    for min_price, max_price, label in ranges:
        if max_price == float('inf'):
            count = category.ads.filter(price__gte=min_price).count()
        else:
            count = category.ads.filter(price__gte=min_price, price__lt=max_price).count()
        print(f"   {label}: {count} ta e'lon")
    print()
    
    # Test search filtering
    print("🔎 QIDIRUV BO'YICHA FILTERLASH:")
    search_terms = ['iPhone', 'Samsung', 'BMW', 'Toyota', 'Nike']
    
    for term in search_terms:
        count = category.ads.filter(
            Q(title__icontains=term) | Q(description__icontains=term)
        ).count()
        if count > 0:
            print(f"   '{term}': {count} ta e'lon topildi")
    print()
    
    # Combined filtering example
    print("🎯 KOMBINATSIYALI FILTERLASH NAMUNASI:")
    location = locations[0] if locations else None
    if location:
        combined_ads = category.ads.filter(
            location=location,
            price__lte=5000000  # 5 mln so'mgacha
        )
        print(f"   {category.name} + {location.name} + 5 mln so'mgacha: {combined_ads.count()} ta e'lon")
        
        # Show some examples
        for ad in combined_ads[:3]:
            print(f"     - {ad.title}: {ad.price:,} so'm")
    print()
    
    print("✅ KATEGORIYA SAHIFASI XUSUSIYATLARI:")
    print("   🏠 Bosh sahifaga qaytish tugmasi")
    print("   📍 Joylashuv bo'yicha filterlash")
    print("   💰 Narx oralig'i bo'yicha filterlash") 
    print("   🔍 Matn bo'yicha qidiruv")
    print("   🧹 Filterlarni tozalash")
    print("   📄 Pagination bilan barcha filterlarni saqlash")
    print()
    print("🎉 Demo tugallandi!")

if __name__ == "__main__":
    from django.db import models
    demo_category_filtering()
