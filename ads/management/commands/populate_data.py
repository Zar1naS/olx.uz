from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ads.models import Category, Location, Ad
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate initial data for the OLX application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create categories
        categories_data = [
            {'name': 'Transport', 'slug': 'transport', 'icon': 'fas fa-car', 'order': 1},
            {'name': 'Elektronika', 'slug': 'electronics', 'icon': 'fas fa-mobile-alt', 'order': 2},
            {'name': 'Ko\'chmas mulk', 'slug': 'real-estate', 'icon': 'fas fa-home', 'order': 3},
            {'name': 'Uy va bog\'', 'slug': 'home', 'icon': 'fas fa-couch', 'order': 4},
            {'name': 'Moda va stil', 'slug': 'fashion', 'icon': 'fas fa-tshirt', 'order': 5},
            {'name': 'Ish', 'slug': 'work', 'icon': 'fas fa-briefcase', 'order': 6},
            {'name': 'Hayvonlar', 'slug': 'animals', 'icon': 'fas fa-paw', 'order': 7},
            {'name': 'Bolalar dunyosi', 'slug': 'children', 'icon': 'fas fa-baby', 'order': 8},
            {'name': 'Biznes va xizmatlar', 'slug': 'business', 'icon': 'fas fa-handshake', 'order': 9},
            {'name': 'Sevimli mashg\'ulot', 'slug': 'hobby', 'icon': 'fas fa-futbol', 'order': 10},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create locations
        locations_data = [
            {'name': 'Toshkent', 'slug': 'tashkent', 'order': 1},
            {'name': 'Samarqand', 'slug': 'samarkand', 'order': 2},
            {'name': 'Buxoro', 'slug': 'bukhara', 'order': 3},
            {'name': 'Namangan', 'slug': 'namangan', 'order': 4},
            {'name': 'Andijon', 'slug': 'andijan', 'order': 5},
            {'name': 'Farg\'ona', 'slug': 'fergana', 'order': 6},
            {'name': 'Qashqadaryo', 'slug': 'kashkadarya', 'order': 7},
            {'name': 'Surxondaryo', 'slug': 'surkhandarya', 'order': 8},
            {'name': 'Jizzax', 'slug': 'jizzakh', 'order': 9},
            {'name': 'Sirdaryo', 'slug': 'sirdarya', 'order': 10},
            {'name': 'Navoiy', 'slug': 'navoi', 'order': 11},
            {'name': 'Xorazm', 'slug': 'khorezm', 'order': 12},
            {'name': 'Qoraqalpog\'iston', 'slug': 'karakalpakstan', 'order': 13},
        ]
        
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(
                slug=loc_data['slug'],
                defaults=loc_data
            )
            if created:
                self.stdout.write(f'Created location: {location.name}')
        
        # Create a demo user if it doesn't exist
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
        
        # Create sample ads
        if not Ad.objects.exists():
            ads_data = [
                {
                    'title': 'iPhone 14 Pro Max 256GB',
                    'description': 'Yangi iPhone 14 Pro Max, 256GB xotira, Space Black rangda. Kafolat bilan.',
                    'category': 'electronics',
                    'location': 'tashkent',
                    'price': Decimal('15000000'),
                    'phone': '+998901234567',
                },
                {
                    'title': 'Toyota Camry 2020',
                    'description': 'Toyota Camry 2020, 2.5L dvigatel, avtomat. Holatı a\'lo, bir qo\'ldan.',
                    'category': 'transport',
                    'location': 'tashkent',
                    'price': Decimal('350000000'),
                    'phone': '+998901234568',
                },
                {
                    'title': '2 xonali kvartira',
                    'description': 'Samarqandda 2 xonali kvartira, 54 kv.m, 3-qavat, yangi ta\'mir.',
                    'category': 'real-estate',
                    'location': 'samarkand',
                    'price': Decimal('85000000'),
                    'phone': '+998901234569',
                },
            ]
            
            for ad_data in ads_data:
                category = Category.objects.get(slug=ad_data['category'])
                location = Location.objects.get(slug=ad_data['location'])
                
                ad = Ad.objects.create(
                    title=ad_data['title'],
                    description=ad_data['description'],
                    category=category,
                    location=location,
                    user=demo_user,
                    price=ad_data['price'],
                    phone=ad_data['phone'],
                )
                self.stdout.write(f'Created ad: {ad.title}')
        
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))
