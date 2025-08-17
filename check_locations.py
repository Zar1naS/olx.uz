#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx.settings')
django.setup()

from ads.models import Location

print("Location statistics:")
print(f"Total locations: {Location.objects.count()}")
print(f"Active locations: {Location.objects.filter(is_active=True).count()}")

print("\nActive locations list:")
for loc in Location.objects.filter(is_active=True).order_by('order', 'name'):
    print(f"- {loc.name} (slug: {loc.slug})")

print("\nFirst 3 locations with details:")
for loc in Location.objects.filter(is_active=True)[:3]:
    print(f"ID: {loc.id}, Name: {loc.name}, Slug: {loc.slug}, Order: {loc.order}, Active: {loc.is_active}")
