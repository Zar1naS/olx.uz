from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ads.models import Category, Location, Ad, AdImage
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample ads data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))

        # Create sample categories
        categories_data = [
            {
                'name': 'Elektron texnikalar',
                'name_ru': 'Электроника',
                'icon': 'fas fa-laptop',
                'description': 'Telefon, kompyuter, televizor va boshqa elektron texnikalar'
            },
            {
                'name': 'Avtomobillar',
                'name_ru': 'Автомобили',
                'icon': 'fas fa-car',
                'description': 'Avtomobillar, mototsikllar va transport vositalari'
            },
            {
                'name': 'Ko\'chmas mulk',
                'name_ru': 'Недвижимость',
                'icon': 'fas fa-home',
                'description': 'Uy, kvartira, ofis va boshqa ko\'chmas mulklar'
            },
            {
                'name': 'Moda va kiyim',
                'name_ru': 'Мода и одежда',
                'icon': 'fas fa-tshirt',
                'description': 'Erkaklar, ayollar va bolalar kiyimlari'
            },
            {
                'name': 'Uy va bog\'',
                'name_ru': 'Дом и сад',
                'icon': 'fas fa-couch',
                'description': 'Mebel, uy jihozlari va bog\' uchun buyumlar'
            },
            {
                'name': 'Sport va dam olish',
                'name_ru': 'Спорт и отдых',
                'icon': 'fas fa-football-ball',
                'description': 'Sport anjomlari va dam olish uchun buyumlar'
            },
            {
                'name': 'Kitoblar va ta\'lim',
                'name_ru': 'Книги и образование',
                'icon': 'fas fa-book',
                'description': 'Kitoblar, darsliklar va ta\'lim materiallari'
            },
            {
                'name': 'Bolalar dunyosi',
                'name_ru': 'Детский мир',
                'icon': 'fas fa-baby',
                'description': 'Bolalar uchun kiyim, o\'yinchoq va boshqa buyumlar'
            },
        ]

        categories = []
        for i, cat_data in enumerate(categories_data):
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'name_ru': cat_data['name_ru'],
                    'icon': cat_data['icon'],
                    'description': cat_data['description'],
                    'order': i
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample locations
        locations_data = [
            'Toshkent',
            'Samarqand',
            'Buxoro',
            'Andijon',
            'Farg\'ona',
            'Namangan',
            'Qashqadaryo',
            'Surxondaryo',
            'Jizzax',
            'Navoiy',
            'Sirdaryo',
            'Xorazm',
            'Qoraqalpog\'iston'
        ]

        locations = []
        for i, loc_name in enumerate(locations_data):
            location, created = Location.objects.get_or_create(
                name=loc_name,
                defaults={'order': i}
            )
            locations.append(location)
            if created:
                self.stdout.write(f'Created location: {location.name}')

        # Create a default user if doesn't exist
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Created default admin user')

        # Sample products data
        sample_ads = [
            # Elektron texnikalar
            {
                'title': 'iPhone 14 Pro 128GB',
                'description': 'Yangi iPhone 14 Pro, 128GB xotira. Barcha aksessuarlar bilan. Kafolat mavjud. Telefon juda yaxshi holatda.',
                'category': 'Elektron texnikalar',
                'price': 12500000,
                'condition': 'excellent',
            },
            {
                'title': 'Samsung Galaxy S23 Ultra',
                'description': 'Samsung Galaxy S23 Ultra 256GB. S Pen bilan. Kamera sifati a\'lo. Hech qanday kamchilik yo\'q.',
                'category': 'Elektron texnikalar',
                'price': 15000000,
                'condition': 'new',
            },
            {
                'title': 'Gaming Laptop ASUS ROG',
                'description': 'ASUS ROG Strix G15. Intel Core i7, 16GB RAM, RTX 3070, 1TB SSD. O\'yin uchun mukammal.',
                'category': 'Elektron texnikalar',
                'price': 20000000,
                'condition': 'excellent',
            },
            {
                'title': 'MacBook Air M2 2022',
                'description': 'MacBook Air M2, 256GB SSD, 8GB RAM. Ishchilar va talabalar uchun ideal. Batareya 18 soatgacha.',
                'category': 'Elektron texnikalar',
                'price': 18000000,
                'condition': 'good',
            },
            
            # Avtomobillar
            {
                'title': 'Chevrolet Nexia 2021',
                'description': 'Chevrolet Nexia 2021 yil, 1.5 litr dvigatel. Probeg 35,000 km. To\'liq texnik ko\'rik o\'tgan.',
                'category': 'Avtomobillar',
                'price': 180000000,
                'condition': 'excellent',
            },
            {
                'title': 'Toyota Camry 2019',
                'description': 'Toyota Camry 2019, V6 dvigatel, avtomat uzatmalar qutisi. Premium salon, barcha qulayliklar.',
                'category': 'Avtomobillar',
                'price': 420000000,
                'condition': 'excellent',
            },
            {
                'title': 'Hyundai Solaris 2020',
                'description': 'Hyundai Solaris 2020, 1.4 litr, mexanika. Ekonomik va ishonchli mashina. Birinchi egasidan.',
                'category': 'Avtomobillar',
                'price': 190000000,
                'condition': 'good',
            },
            
            # Ko'chmas mulk
            {
                'title': '3-xonali kvartira, Toshkent markazi',
                'description': '3-xonali kvartira, 85 kv.m, 5-qavat, Toshkent markazida. Euro ta\'mir, barcha qulayliklar.',
                'category': 'Ko\'chmas mulk',
                'price': 2500000000,
                'condition': 'excellent',
            },
            {
                'title': 'Hovli uyi, Samarqandda',
                'description': 'Hovli uyi 150 kv.m, 6 sotix yer. Bog\', hovuz, garage mavjud. Tabiat qo\'ynida tinchlik.',
                'category': 'Ko\'chmas mulk',
                'price': 800000000,
                'condition': 'good',
            },
            
            # Moda va kiyim
            {
                'title': 'Nike Air Jordan krossovkalari',
                'description': 'Asl Nike Air Jordan, 42 o\'lcham. Yangi, hali ishlatilmagan. Box va barcha aksessuarlar bilan.',
                'category': 'Moda va kiyim',
                'price': 2500000,
                'condition': 'new',
            },
            {
                'title': 'Adidas ko\'ylagi va shim',
                'description': 'Adidas sport kostyumi, L o\'lcham. Yuqori sifatli material. Sport va kundalik kiyish uchun.',
                'category': 'Moda va kiyim',
                'price': 850000,
                'condition': 'excellent',
            },
            
            # Uy va bog'
            {
                'title': 'Divan to\'plami, 3+2+1',
                'description': 'Zamonaviy divan to\'plami, yumshoq va qulay. Rangi jigarrang. Yaxshi holatda.',
                'category': 'Uy va bog\'',
                'price': 8500000,
                'condition': 'good',
            },
            {
                'title': 'Oshxona mebeli to\'plami',
                'description': 'Oshxona uchun to\'liq mebel to\'plami. Zamonaviy dizayn, barcha jihozlar uchun joy.',
                'category': 'Uy va bog\'',
                'price': 12000000,
                'condition': 'excellent',
            },
            
            # Sport va dam olish
            {
                'title': 'Velosiped Trek Mountain Bike',
                'description': 'Trek tog\' velosipedi, 21 tezlik. Disk tormozlar, amortizator. Sayohat va sport uchun.',
                'category': 'Sport va dam olish',
                'price': 4500000,
                'condition': 'good',
            },
            {
                'title': 'Futbol to\'pi FIFA',
                'description': 'Rasmiy FIFA futbol to\'pi. Professional o\'yinlar uchun sifat. Yangi, ishlatilmagan.',
                'category': 'Sport va dam olish',
                'price': 350000,
                'condition': 'new',
            },
            
            # Kitoblar va ta'lim
            {
                'title': 'Python dasturlash kitobi',
                'description': 'Python dasturlash tilini o\'rganish uchun to\'liq qo\'llanma. Uzbek va ingliz tilida.',
                'category': 'Kitoblar va ta\'lim',
                'price': 150000,
                'condition': 'excellent',
            },
            {
                'title': 'IELTS imtihoni uchun kitoblar',
                'description': 'IELTS imtihoniga tayyorgarlik uchun to\'liq kitoblar to\'plami. Audio CD bilan.',
                'category': 'Kitoblar va ta\'lim',
                'price': 250000,
                'condition': 'good',
            },
            
            # Bolalar dunyosi
            {
                'title': 'Bolalar velosipedi',
                'description': 'Bolalar uchun velosiped, 4-7 yosh. Qo\'shimcha g\'ildiraklar, qo\'ng\'iroq va sari rang.',
                'category': 'Bolalar dunyosi',
                'price': 1200000,
                'condition': 'good',
            },
            {
                'title': 'LEGO konstruktor to\'plami',
                'description': 'LEGO City konstruktor to\'plami. 500+ detal. Bolalar uchun rivojlantiruvchi o\'yinchoq.',
                'category': 'Bolalar dunyosi',
                'price': 650000,
                'condition': 'excellent',
            },
        ]

        # Create sample ads
        phones = ['+998901234567', '+998977654321', '+998935551234', '+998901111111', '+998909876543']
        
        for ad_data in sample_ads:
            # Find category
            category = None
            for cat in categories:
                if cat.name == ad_data['category']:
                    category = cat
                    break
            
            if not category:
                continue
                
            # Random location and user
            location = random.choice(locations)
            phone = random.choice(phones)
            
            ad, created = Ad.objects.get_or_create(
                title=ad_data['title'],
                defaults={
                    'description': ad_data['description'],
                    'category': category,
                    'location': location,
                    'user': user,
                    'price': Decimal(ad_data['price']),
                    'condition': ad_data['condition'],
                    'phone': phone,
                    'is_negotiable': random.choice([True, False]),
                    'views_count': random.randint(10, 500),
                }
            )
            
            if created:
                self.stdout.write(f'Created ad: {ad.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {Category.objects.count()} categories\n'
                f'- {Location.objects.count()} locations\n'
                f'- {Ad.objects.count()} ads'
            )
        )
