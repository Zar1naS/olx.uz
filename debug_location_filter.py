#!/usr/bin/env python
"""
Location filterlash muammosini debug qilish uchun script.
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ads.models import Category, Location, Ad

def debug_location_filtering():
    print("🔍 LOCATION FILTERING DEBUG")
    print("=" * 50)
    
    # Get test data
    elektron = Category.objects.get(name='Elektron texnikalar')
    samarqand = Location.objects.get(name='Samarqand')
    
    print(f"📱 Category: {elektron.name} (slug: {elektron.slug})")
    print(f"📍 Location: {samarqand.name} (slug: {samarqand.slug})")
    print()
    
    # Test 1: Direct database query
    print("TEST 1: Direct database query")
    all_ads = elektron.ads.filter(is_active=True)
    filtered_ads = all_ads.filter(location=samarqand)
    
    print(f"All ads: {all_ads.count()}")
    print(f"Samarqand ads: {filtered_ads.count()}")
    print("Samarqand ads:")
    for ad in filtered_ads:
        print(f"  - {ad.title} (Location: {ad.location.name})")
    print()
    
    # Test 2: Simulate GET request
    print("TEST 2: Simulate GET request with Django Client")
    client = Client()
    
    # Create URL
    category_url = reverse('ads:category', kwargs={'slug': elektron.slug})
    full_url = f"{category_url}?location={samarqand.slug}"
    
    print(f"Category URL: {category_url}")
    print(f"Full URL with filter: {full_url}")
    
    # Make request
    response = client.get(full_url)
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        if hasattr(response, 'context') and response.context:
            context = response.context
            ads = context['ads']
            selected_location = context.get('selected_location')
            debug_info = context.get('debug_info', {})
            
            print(f"Selected location: {selected_location}")
            print(f"Debug info: {debug_info}")
            print(f"Ads count in response: {ads.paginator.count if hasattr(ads, 'paginator') else len(ads)}")
            
            print("Ads in response:")
            for ad in ads:
                print(f"  - {ad.title} (Location: {ad.location.name})")
        else:
            print("✅ Response OK, but no context available (possibly due to template rendering)")
            # Check if filtering text is in response content
            response_text = response.content.decode('utf-8')
            if 'Samarqand viloyatidagi' in response_text:
                print("✅ Location filtering text found in response")
            else:
                print("❌ Location filtering text NOT found in response")
    else:
        print(f"❌ Request failed with status {response.status_code}")
    
    print()
    
    # Test 3: Check all locations and their ads
    print("TEST 3: All locations and their ad counts in this category")
    for location in Location.objects.all()[:5]:
        count = elektron.ads.filter(is_active=True, location=location).count()
        print(f"  {location.name} ({location.slug}): {count} ads")
    
    print()
    print("🎯 DEBUGGING COMPLETE")

if __name__ == "__main__":
    debug_location_filtering()
