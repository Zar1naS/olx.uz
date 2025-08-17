from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ads.models import Category, Location, Ad
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Add more products to categories that have less than 20 items'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Balancing categories to have at least 20 products each...'))

        # Get all categories with less than 20 products
        categories_to_balance = []
        for category in Category.objects.all():
            ads_count = category.ads.count()
            if ads_count < 20:
                needed = 20 - ads_count
                categories_to_balance.append((category, needed))
                self.stdout.write(f'{category.name}: {ads_count} ta, {needed} ta qo\'shish kerak')

        # Get user and locations
        user = User.objects.get(username='admin')
        locations = list(Location.objects.all())
        phones = ['+998901234567', '+998977654321', '+998935551234', '+998901111111', '+998909876543']

        # Additional products for each category
        additional_products = {
            'Elektron texnikalar': [
                ('Xiaomi Redmi Note 12', 'Xiaomi Redmi Note 12 Pro, 128GB xotira, 6GB RAM. 108MP kamera, 5000mAh batareya.', 4500000, 'new'),
                ('Samsung Galaxy A54', 'Samsung Galaxy A54, 256GB, Super AMOLED ekran, 50MP kamera, 5000mAh batareya.', 6800000, 'excellent'),
                ('OPPO Find N2', 'OPPO Find N2 buklanadigan telefon, 256GB xotira, premium dizayn, ikki ekranli.', 18500000, 'new'),
                ('Huawei P50 Pro', 'Huawei P50 Pro, Leica kameralar, 256GB, professional fotosurat uchun mukammal.', 11200000, 'excellent'),
                ('OnePlus 11', 'OnePlus 11, 256GB, Snapdragon 8 Gen 2, 100W tez quvvatlash, gaming uchun ideal.', 9800000, 'excellent'),
                ('iPhone 13 Mini', 'iPhone 13 Mini, 128GB, A15 Bionic chip, kompakt va kuchli, barcha ranglar.', 10200000, 'good'),
                ('Realme GT 3', 'Realme GT 3, 240W tez quvvatlash, 256GB xotira, gaming performance.', 5600000, 'new'),
                ('Vivo X90 Pro', 'Vivo X90 Pro, Zeiss kameralar, 256GB, professional video va foto.', 12800000, 'excellent'),
                ('Nothing Phone 2', 'Nothing Phone 2, 256GB, noyob dizayn, LED yoritgich paneli.', 8900000, 'new'),
                ('Google Pixel 7', 'Google Pixel 7, 128GB, eng yaxshi Android tajriba, Google AI kameralar.', 8500000, 'excellent'),
                ('Sony Xperia 1 V', 'Sony Xperia 1 V, professional kameralar, 4K ekran, content creation uchun.', 15600000, 'new'),
                ('Motorola Edge 40', 'Motorola Edge 40, curved ekran, 256GB, toza Android tajriba.', 6200000, 'excellent'),
                ('Asus ROG Phone 7', 'Asus ROG Phone 7, gaming telefon, 512GB, air cooling system.', 16800000, 'new'),
                ('Honor Magic 5 Pro', 'Honor Magic 5 Pro, 512GB, premium build quality, professional kameralar.', 13400000, 'excellent'),
                ('TCL 30 5G', 'TCL 30 5G, budget-friendly, 128GB, 5G aloqa, yaxshi kameralar.', 3200000, 'good'),
                ('Infinix Note 12', 'Infinix Note 12, katta batareya, 128GB xotira, MediaTek processor.', 2800000, 'new'),
            ],
            
            'Avtomobillar': [
                ('BMW X5 2020', 'BMW X5 2020, 3.0 litr twin-turbo, premium interior, to\'liq elektron paket.', 850000000, 'excellent'),
                ('Mercedes-Benz E-Class', 'Mercedes E-Class 2019, 2.0 litr turbo, avtomat, leather salon, sunroof.', 720000000, 'excellent'),
                ('Audi Q7 2021', 'Audi Q7 2021, 3.0 TFSI, Quattro, 7 o\'rindiq, virtual cockpit, premium.', 980000000, 'excellent'),
                ('Lexus RX 350', 'Lexus RX 350 2020, hybrid, AWD, premium comfort, ishonchli va ekonomik.', 680000000, 'excellent'),
                ('Porsche Cayenne', 'Porsche Cayenne 2019, V6 turbo, sport paket, premium interior, ideal holat.', 1200000000, 'excellent'),
                ('Range Rover Evoque', 'Range Rover Evoque 2021, 2.0 turbo, AWD, panoramic roof, luxury.', 850000000, 'excellent'),
                ('Volvo XC90 2020', 'Volvo XC90 2020, T6 AWD, 7 seats, safety paket, Scandinavian luxury.', 780000000, 'excellent'),
                ('Genesis GV70', 'Genesis GV70 2022, premium Korean SUV, V6 engine, luxury interior.', 650000000, 'new'),
                ('Infiniti QX60', 'Infiniti QX60 2021, V6 CVT, 7 seats, comfort va family uchun ideal.', 580000000, 'excellent'),
                ('Acura MDX 2020', 'Acura MDX 2020, V6 SH-AWD, 7 seats, sport va luxury kombinatsiya.', 620000000, 'excellent'),
                ('Cadillac XT6', 'Cadillac XT6 2021, V6 AWD, American luxury, spacious interior.', 680000000, 'excellent'),
                ('Lincoln Navigator', 'Lincoln Navigator 2020, V6 twin-turbo, full-size luxury SUV, 8 seats.', 950000000, 'excellent'),
                ('Jeep Grand Cherokee', 'Jeep Grand Cherokee 2021, V6 4x4, Laredo trim, off-road capability.', 520000000, 'excellent'),
                ('Ford Explorer 2022', 'Ford Explorer 2022, EcoBoost turbo, 7 seats, family SUV, reliable.', 480000000, 'new'),
                ('Chevrolet Tahoe', 'Chevrolet Tahoe 2021, V8 engine, full-size SUV, towing capacity.', 720000000, 'excellent'),
                ('GMC Yukon 2020', 'GMC Yukon 2020, V8 4WD, premium interior, large family SUV.', 680000000, 'excellent'),
                ('Nissan Armada', 'Nissan Armada 2021, V8 4WD, 8 seats, powerful va spacious.', 580000000, 'excellent'),
            ],
            
            'Moda va kiyim': [
                ('Zara erkaklar ko\'ylagi', 'Zara premium erkaklar ko\'ylagi, 100% paxta, classic fit, oq rang.', 450000, 'new'),
                ('H&M ayollar kurtka', 'H&M ayollar qishki kurtka, waterproof, stylish design, S-XL o\'lchamlar.', 850000, 'excellent'),
                ('Gucci sumka', 'Original Gucci leather sumka, handmade, luxury brand, authenticity bilan.', 15000000, 'excellent'),
                ('Louis Vuitton belt', 'Louis Vuitton erkaklar kamari, genuine leather, signature buckle.', 8500000, 'new'),
                ('Chanel parfyum', 'Chanel No. 5 parfyum, 100ml, original, luxury packaging bilan.', 2800000, 'new'),
                ('Nike Air Max sneakers', 'Nike Air Max 270, erkaklar uchun, comfortable, 41-45 o\'lchamlar.', 1800000, 'new'),
                ('Adidas Ultraboost', 'Adidas Ultraboost 22, running shoes, boost technology, premium.', 2200000, 'excellent'),
                ('Puma tracksuit', 'Puma erkaklar sport kostyumi, breathable fabric, modern design.', 950000, 'new'),
                ('Under Armour hoodie', 'Under Armour hoodie, premium cotton, athletic fit, L-XXL.', 680000, 'excellent'),
                ('Levi\'s jeans', 'Original Levi\'s 501 jeans, classic fit, premium denim, 30-38 waist.', 1200000, 'good'),
                ('Tommy Hilfiger polo', 'Tommy Hilfiger polo shirt, cotton blend, classic American style.', 750000, 'excellent'),
                ('Calvin Klein underwear', 'Calvin Klein boxers set, premium cotton, 3-pack, comfortable.', 480000, 'new'),
                ('Hugo Boss suit', 'Hugo Boss erkaklar kostyumi, wool blend, tailored fit, professional.', 8500000, 'excellent'),
                ('Armani watch', 'Armani erkaklar soati, stainless steel, water resistant, luxury.', 3200000, 'new'),
                ('Ray-Ban sunglasses', 'Ray-Ban Aviator classic, UV protection, original, unisex.', 1800000, 'excellent'),
                ('Converse sneakers', 'Converse Chuck Taylor All Star, high-top, classic design, barcha ranglar.', 850000, 'good'),
                ('Vans shoes', 'Vans Old Skool, skate shoes, durable, street style, 36-45 size.', 950000, 'excellent'),
                ('New Balance running', 'New Balance 990v5, premium running shoes, made in USA, comfort.', 2800000, 'new'),
            ],
            
            'Sport va dam olish': [
                ('Professional tennis racket', 'Wilson Pro Staff tennis racket, professional level, 300g, grip 2.', 1200000, 'excellent'),
                ('Boxing gloves set', 'Everlast boxing gloves, 12oz, professional training, leather.', 850000, 'new'),
                ('Yoga mat premium', 'Manduka yoga mat, non-slip, eco-friendly, 6mm thick, professional.', 450000, 'excellent'),
                ('Dumbbell set', 'Adjustable dumbbell set, 5-50kg per dumbbell, home gym equipment.', 2800000, 'new'),
                ('Treadmill electric', 'Electric treadmill, 2.5HP motor, LCD display, folding design.', 8500000, 'excellent'),
                ('Bicycle helmet', 'Specialized bicycle helmet, MIPS technology, ventilated, safety certified.', 680000, 'new'),
                ('Swimming goggles', 'Speedo swimming goggles, anti-fog, UV protection, competitive.', 280000, 'excellent'),
                ('Basketball official', 'Spalding official basketball, leather, NBA approved, indoor/outdoor.', 420000, 'new'),
                ('Fishing rod set', 'Shakespeare fishing rod set, reel included, beginners to advanced.', 950000, 'excellent'),
                ('Golf club set', 'Callaway golf club set, iron set 4-PW, right hand, intermediate.', 12500000, 'excellent'),
                ('Skateboard complete', 'Element skateboard complete, 8.0 deck, ABEC 7 bearings, street.', 1800000, 'new'),
                ('Badminton racket', 'Yonex badminton racket, carbon fiber, professional tournament grade.', 1500000, 'excellent'),
                ('Table tennis paddle', 'Butterfly table tennis paddle, 5-star, tournament approved, grip.', 850000, 'new'),
                ('Rock climbing shoes', 'La Sportiva climbing shoes, aggressive downturn, indoor/outdoor.', 2200000, 'excellent'),
                ('Camping tent 4-person', '4-person camping tent, waterproof, easy setup, family camping.', 1200000, 'new'),
                ('Hiking backpack', 'Osprey hiking backpack, 65L capacity, hydration compatible, comfortable.', 3200000, 'excellent'),
                ('Kayak paddle', 'Werner kayak paddle, carbon fiber, adjustable length, lightweight.', 1800000, 'new'),
                ('Surfboard beginner', 'Foam surfboard, 9ft beginner board, soft top, stable va safe.', 4500000, 'excellent'),
            ],
            
            'Kitoblar va ta\'lim': [
                ('Uzbek adabiyoti to\'plami', 'Uzbek klassik adabiyoti to\'liq to\'plami, 20 jildlik, yangi nashr.', 1200000, 'new'),
                ('English Grammar Book', 'Complete English Grammar, intermediate to advanced, exercises bilan.', 180000, 'excellent'),
                ('Mathematics textbook', 'Advanced Mathematics, university level, solutions manual bilan.', 350000, 'new'),
                ('Computer Science basics', 'Introduction to Computer Science, Python examples, beginner friendly.', 280000, 'excellent'),
                ('Business Management', 'Modern Business Management principles, case studies bilan, practical.', 420000, 'new'),
                ('Medical terminology', 'Medical terminology dictionary, illustrated, students uchun ideal.', 380000, 'excellent'),
                ('Art history book', 'World Art History, full color illustrations, comprehensive coverage.', 680000, 'new'),
                ('Cooking masterclass', 'Professional cooking techniques, recipe book, photo instructions.', 450000, 'excellent'),
                ('Psychology textbook', 'Introduction to Psychology, latest edition, research-based content.', 520000, 'new'),
                ('Economics principles', 'Microeconomics and Macroeconomics, university textbook, examples.', 480000, 'excellent'),
                ('Chemistry laboratory', 'Chemistry lab manual, experiments va procedures, safety guide.', 320000, 'new'),
                ('Physics problems', 'Physics problem solving guide, step-by-step solutions, exam prep.', 380000, 'excellent'),
                ('Biology encyclopedia', 'Complete biology encyclopedia, illustrated, reference book.', 750000, 'new'),
                ('History of Uzbekistan', 'Comprehensive Uzbek history, from ancient times to modern day.', 420000, 'excellent'),
                ('Language learning set', 'Korean language learning set, textbook + audio CDs, beginner.', 680000, 'new'),
                ('SAT preparation', 'SAT exam preparation guide, practice tests, strategies included.', 380000, 'excellent'),
                ('TOEFL study guide', 'TOEFL iBT preparation, listening + speaking + reading + writing.', 450000, 'new'),
                ('GRE test prep', 'GRE General Test preparation, quantitative + verbal + analytical.', 520000, 'excellent'),
            ]
        }

        # Add products to categories that need them
        for category, needed_count in categories_to_balance:
            if category.name in additional_products:
                products = additional_products[category.name]
                
                # Add products up to the needed count
                for i in range(min(needed_count, len(products))):
                    product = products[i]
                    title, description, price, condition = product
                    
                    location = random.choice(locations)
                    phone = random.choice(phones)
                    
                    ad, created = Ad.objects.get_or_create(
                        title=title,
                        defaults={
                            'description': description,
                            'category': category,
                            'location': location,
                            'user': user,
                            'price': Decimal(price),
                            'condition': condition,
                            'phone': phone,
                            'is_negotiable': random.choice([True, False]),
                            'views_count': random.randint(10, 300),
                            'is_featured': random.choice([True, False]) if random.random() < 0.2 else False,
                            'is_vip': random.choice([True, False]) if random.random() < 0.1 else False,
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  + {category.name}: {title}')

        # Final count check
        self.stdout.write(self.style.SUCCESS('\nYANGILANGAN NATIJALAR:'))
        for category in Category.objects.all():
            count = category.ads.count()
            status = '✅' if count >= 20 else '❌'
            self.stdout.write(f'{status} {category.name}: {count} ta mahsulot')

        self.stdout.write(
            self.style.SUCCESS('\nBarcha kategoriyalar muvozanatlandi!')
        )
