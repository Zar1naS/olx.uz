import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from ads.models import Category, Location, Ad, AdImage
from PIL import Image, ImageDraw, ImageFont
import io

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample ads for all categories with images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of ads per category (default: 20)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data for different categories
        sample_data = {
            'electronics': [
                {'title': 'iPhone 15 Pro Max', 'price': 15000000, 'description': 'Yangi iPhone 15 Pro Max, 256GB, barcha ranglarda mavjud.'},
                {'title': 'Samsung Galaxy S24', 'price': 12000000, 'description': 'Samsung Galaxy S24, 128GB, kafolat bilan.'},
                {'title': 'MacBook Air M2', 'price': 18000000, 'description': 'MacBook Air M2, 13-inch, 256GB SSD, ideal ish uchun.'},
                {'title': 'PlayStation 5', 'price': 8000000, 'description': 'PlayStation 5, yangi, barcha aksessuarlar bilan.'},
                {'title': 'iPad Pro 2024', 'price': 14000000, 'description': 'iPad Pro 2024, 11-inch, Apple Pencil bilan.'},
                {'title': 'Xiaomi 14', 'price': 9000000, 'description': 'Xiaomi 14, 256GB, kamera zo\'r.'},
                {'title': 'AirPods Pro', 'price': 3500000, 'description': 'AirPods Pro, shovqin yutish funksiyasi bilan.'},
                {'title': 'Dell XPS 13', 'price': 16000000, 'description': 'Dell XPS 13, Intel i7, 16GB RAM.'},
                {'title': 'Nintendo Switch', 'price': 4500000, 'description': 'Nintendo Switch, o\'yinlar bilan.'},
                {'title': 'Samsung TV 55"', 'price': 7000000, 'description': '55 dyuymli Smart TV, 4K, HDR.'},
            ],
            'real-estate': [
                {'title': '3-xonali kvartira', 'price': 120000000, 'description': '3-xonali kvartira, 90 kv.m, yangi bino.'},
                {'title': 'Hovli uy', 'price': 250000000, 'description': 'Hovli uy, 6 sotix, barcha qulayliklar.'},
                {'title': '2-xonali kvartira', 'price': 80000000, 'description': '2-xonali kvartira, shahar markazida.'},
                {'title': 'Ofis binosi', 'price': 500000000, 'description': 'Ofis binosi, 200 kv.m, biznes uchun.'},
                {'title': 'Dachi', 'price': 150000000, 'description': 'Dachi, 10 sotix, mevali daraxtlar.'},
                {'title': 'Penthouse', 'price': 300000000, 'description': 'Penthouse, tom qavat, shahar manzarasi.'},
                {'title': 'Studio kvartira', 'price': 45000000, 'description': 'Studio kvartira, 35 kv.m, yangiy ta\'mir.'},
                {'title': 'Tijorat binosi', 'price': 800000000, 'description': 'Tijorat binosi, asosiy yo\'lda.'},
                {'title': 'Yer uchastkasi', 'price': 50000000, 'description': 'Yer uchastkasi, 5 sotix, qurilish uchun.'},
                {'title': '4-xonali kvartira', 'price': 180000000, 'description': '4-xonali kvartira, elite uyda.'},
            ],
            'transport': [
                {'title': 'Toyota Camry 2022', 'price': 350000000, 'description': 'Toyota Camry 2022, avtomatik, to\'liq konfiguratsiya.'},
                {'title': 'BMW X5 2021', 'price': 800000000, 'description': 'BMW X5 2021, full option, ideal holatda.'},
                {'title': 'Mercedes E-Class', 'price': 600000000, 'description': 'Mercedes E-Class, 2020-yil, luxury.'},
                {'title': 'Hyundai Tucson', 'price': 400000000, 'description': 'Hyundai Tucson, 2023, kafolat bilan.'},
                {'title': 'Lexus RX 350', 'price': 900000000, 'description': 'Lexus RX 350, premium klass.'},
                {'title': 'Honda Accord', 'price': 300000000, 'description': 'Honda Accord, ishonchli mashina.'},
                {'title': 'Audi A4', 'price': 450000000, 'description': 'Audi A4, sport versiya.'},
                {'title': 'Tesla Model 3', 'price': 700000000, 'description': 'Tesla Model 3, elektr mashina.'},
                {'title': 'Volkswagen Polo', 'price': 220000000, 'description': 'Volkswagen Polo, yangi.'},
                {'title': 'KIA Sportage', 'price': 380000000, 'description': 'KIA Sportage, krossover.'},
            ],
            'home': [
                {'title': 'Kir yuvish mashinasi', 'price': 4500000, 'description': 'Samsung kir yuvish mashinasi, 8kg.'},
                {'title': 'Muzlatgich', 'price': 6000000, 'description': 'LG muzlatgich, 2-kamerali, A+ klass.'},
                {'title': 'Divani to\'plam', 'price': 8000000, 'description': 'Divan to\'plam, teri, 3+2+1.'},
                {'title': 'Yotoq xonasi mebeli', 'price': 12000000, 'description': 'Yotoq xonasi mebeli, to\'liq komplekt.'},
                {'title': 'Oshxona mebeli', 'price': 15000000, 'description': 'Oshxona mebeli, zamonaviy dizayn.'},
                {'title': 'Konditsioner', 'price': 3500000, 'description': 'Konditsioner, 24000 BTU, inverter.'},
                {'title': 'Stol-stul to\'plami', 'price': 5000000, 'description': 'Ovqat stoli va 6 ta stul.'},
                {'title': 'Shkaf', 'price': 4000000, 'description': 'Kiyim shkafi, 4-eshikli.'},
                {'title': 'Matras', 'price': 2500000, 'description': 'Ortopedik matras, 2-kishi uchun.'},
                {'title': 'Luster', 'price': 800000, 'description': 'Kristall luster, zamonaviy.'},
            ],
            'fashion': [
                {'title': 'Nike Air Max', 'price': 1800000, 'description': 'Nike Air Max, original, 42 razmer.'},
                {'title': 'Adidas Ultraboost', 'price': 2200000, 'description': 'Adidas Ultraboost, yangi kolleksiya.'},
                {'title': 'Zara ko\'ylagi', 'price': 800000, 'description': 'Zara ko\'ylagi, premium sifat.'},
                {'title': 'Leather jacket', 'price': 3500000, 'description': 'Teri kurtka, haqiqiy teri.'},
                {'title': 'Rolex soat', 'price': 25000000, 'description': 'Rolex soat, original, kafolat bilan.'},
                {'title': 'Gucci sumka', 'price': 5000000, 'description': 'Gucci sumka, ayollar uchun.'},
                {'title': 'Calvin Klein shim', 'price': 1200000, 'description': 'Calvin Klein jinsi shim.'},
                {'title': 'H&M sviter', 'price': 600000, 'description': 'H&M sviter, qish uchun.'},
                {'title': 'Ray-Ban ko\'zoynak', 'price': 1500000, 'description': 'Ray-Ban quyosh ko\'zoynagi.'},
                {'title': 'Puma krossovka', 'price': 1600000, 'description': 'Puma krossovka, sport uchun.'},
            ]
        }

        # Get all categories
        categories = Category.objects.all()
        locations = list(Location.objects.all())
        users = list(User.objects.all())

        self.stdout.write(f"Barcha kategoriyalarga {count} tadan e'lon yaratish boshlandi...")

        total_created = 0
        
        for category in categories:
            self.stdout.write(f"\n{category.name} kategoriyasi uchun e'lonlar yaratilmoqda...")
            
            # Get sample data for this category or use default
            category_samples = sample_data.get(category.slug, [
                {'title': f'{category.name} mahsuloti', 'price': 1000000, 'description': f'{category.name} kategoriyasidagi mahsulot.'}
            ] * 10)
            
            created_count = 0
            for i in range(count):
                try:
                    # Choose random sample data
                    sample = random.choice(category_samples)
                    
                    # Create unique title
                    title = f"{sample['title']} #{i+1}"
                    
                    # Random price variation
                    base_price = sample['price']
                    price_variation = random.uniform(0.8, 1.3)
                    price = Decimal(str(int(base_price * price_variation)))
                    
                    # Create ad
                    ad = Ad.objects.create(
                        title=title,
                        description=sample['description'] + f" E'lon #{i+1}",
                        category=category,
                        location=random.choice(locations),
                        user=random.choice(users),
                        price=price,
                        condition=random.choice(['new', 'excellent', 'good', 'fair']),
                        phone=f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
                        is_negotiable=random.choice([True, False]),
                        is_featured=random.choice([True, False]) if random.random() < 0.2 else False,
                        is_vip=random.choice([True, False]) if random.random() < 0.1 else False,
                        views_count=random.randint(0, 100),
                    )
                    
                    # Create sample image
                    self.create_sample_image(ad, category.name)
                    
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Xatolik yuz berdi: {str(e)}')
                    )
                    continue
            
            total_created += created_count
            self.stdout.write(
                self.style.SUCCESS(f'{category.name}: {created_count} ta e\'lon yaratildi')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nJami {total_created} ta e\'lon muvaffaqiyatli yaratildi!')
        )

    def create_sample_image(self, ad, category_name):
        """Create a sample image for the ad"""
        try:
            # Create image with PIL
            img = Image.new('RGB', (800, 600), color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                # Try to load a font, fallback to default if not available
                font = ImageFont.load_default()
            except:
                font = None
            
            text = f"{category_name}\n{ad.title[:30]}"
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), text, font=font) if font else (0, 0, 100, 50)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (800 - text_width) // 2
            y = (600 - text_height) // 2
            
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            # Save to memory
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_io.seek(0)
            
            # Create AdImage
            image_name = f"{ad.slug}_{random.randint(1000, 9999)}.jpg"
            ad_image = AdImage.objects.create(
                ad=ad,
                is_main=True,
                order=1
            )
            
            ad_image.image.save(
                image_name,
                ContentFile(img_io.getvalue()),
                save=True
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Rasm yaratishda xatolik: {str(e)}')
            )
