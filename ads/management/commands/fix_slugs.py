from django.core.management.base import BaseCommand
from django.utils.text import slugify
from ads.models import Ad, Category, Location
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix empty slugs and create proper sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fixing slugs and creating sample data...'))
        
        # Fix any ads with empty slugs
        ads_without_slugs = Ad.objects.filter(slug='')
        for ad in ads_without_slugs:
            base_slug = slugify(ad.title)
            slug = base_slug
            counter = 1
            while Ad.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            ad.slug = slug
            ad.save()
            self.stdout.write(f'Fixed slug for ad: {ad.title} -> {ad.slug}')
        
        # Get or create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'phone': '+998901234567',
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write('Created demo user')
        
        # Create sample ads if we don't have many
        if Ad.objects.count() < 5:
            # Ensure we have required categories and locations
            transport_cat, _ = Category.objects.get_or_create(
                slug='transport',
                defaults={
                    'name': 'Transport',
                    'icon': 'fas fa-car',
                    'order': 1
                }
            )
            
            electronics_cat, _ = Category.objects.get_or_create(
                slug='electronics', 
                defaults={
                    'name': 'Elektronika',
                    'icon': 'fas fa-mobile-alt', 
                    'order': 2
                }
            )
            
            real_estate_cat, _ = Category.objects.get_or_create(
                slug='real-estate',
                defaults={
                    'name': "Ko'chmas mulk",
                    'icon': 'fas fa-home',
                    'order': 3
                }
            )
            
            tashkent_loc, _ = Location.objects.get_or_create(
                slug='tashkent',
                defaults={
                    'name': 'Toshkent',
                    'order': 1
                }
            )
            
            samarkand_loc, _ = Location.objects.get_or_create(
                slug='samarkand',
                defaults={
                    'name': 'Samarqand',
                    'order': 2
                }
            )
            
            # Create sample ads
            sample_ads = [
                {
                    'title': 'iPhone 14 Pro Max 256GB',
                    'description': 'Yangi iPhone 14 Pro Max, 256GB xotira, Space Black rangda. Kafolat bilan.',
                    'category': electronics_cat,
                    'location': tashkent_loc,
                    'price': Decimal('15000000'),
                    'phone': '+998901234567',
                },
                {
                    'title': 'Toyota Camry 2020',
                    'description': "Toyota Camry 2020, 2.5L dvigatel, avtomat. Holatı a'lo, bir qo'ldan.",
                    'category': transport_cat,
                    'location': tashkent_loc,
                    'price': Decimal('350000000'),
                    'phone': '+998901234568',
                },
                {
                    'title': '2 xonali kvartira',
                    'description': "Samarqandda 2 xonali kvartira, 54 kv.m, 3-qavat, yangi ta'mir.",
                    'category': real_estate_cat,
                    'location': samarkand_loc,
                    'price': Decimal('85000000'),
                    'phone': '+998901234569',
                },
            ]
            
            for ad_data in sample_ads:
                # Check if this ad already exists (by title)
                if not Ad.objects.filter(title=ad_data['title']).exists():
                    ad = Ad.objects.create(
                        title=ad_data['title'],
                        description=ad_data['description'],
                        category=ad_data['category'],
                        location=ad_data['location'],
                        user=demo_user,
                        price=ad_data['price'],
                        phone=ad_data['phone'],
                    )
                    self.stdout.write(f'Created sample ad: {ad.title}')
        
        self.stdout.write(self.style.SUCCESS('Slugs fixed and sample data created successfully!'))
