from django.core.management.base import BaseCommand
from ads.models import Ad, AdImage
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io
import random

class Command(BaseCommand):
    help = 'Add placeholder images to sample ads'

    def create_placeholder_image(self, text, size=(800, 600), bg_color=None):
        """Create a simple placeholder image with text"""
        if bg_color is None:
            # Random pleasant colors
            colors = [
                (52, 152, 219),   # Blue
                (155, 89, 182),   # Purple  
                (46, 204, 113),   # Green
                (241, 196, 15),   # Yellow
                (230, 126, 34),   # Orange
                (231, 76, 60),    # Red
                (149, 165, 166),  # Gray
                (26, 188, 156),   # Turquoise
            ]
            bg_color = random.choice(colors)
        
        # Create image
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a basic font
        try:
            # For Windows, try a common font
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Calculate text position (center)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (size[0] - text_width) / 2
        y = (size[1] - text_height) / 2
        
        # Draw text
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        return img

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding placeholder images to sample ads...'))

        # Get ads that don't have images
        ads_without_images = Ad.objects.filter(images__isnull=True).distinct()
        
        image_mapping = {
            'iPhone': 'iPhone 14 Pro',
            'Samsung': 'Galaxy S23',
            'Gaming': 'Gaming Laptop',
            'MacBook': 'MacBook Air',
            'Chevrolet': 'Nexia 2021',
            'Toyota': 'Camry 2019',
            'Hyundai': 'Solaris 2020',
            'kvartira': '3-Room Apt',
            'uyi': 'House',
            'Nike': 'Air Jordan',
            'Adidas': 'Sport Set',
            'Divan': 'Sofa Set',
            'Oshxona': 'Kitchen Set',
            'Velosiped': 'Mountain Bike',
            'Futbol': 'FIFA Ball',
            'Python': 'Programming',
            'IELTS': 'IELTS Books',
            'velosipedi': 'Kids Bike',
            'LEGO': 'LEGO Set',
        }
        
        for ad in ads_without_images[:20]:  # Limit to first 20 ads
            # Determine image text based on title
            image_text = ad.title
            for key, value in image_mapping.items():
                if key in ad.title:
                    image_text = value
                    break
            
            # Create placeholder image
            img = self.create_placeholder_image(image_text[:15])  # Limit text length
            
            # Convert PIL image to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=85)
            img_buffer.seek(0)
            
            # Create AdImage instance
            ad_image = AdImage(
                ad=ad,
                is_main=True,
                order=0
            )
            
            # Save image file
            filename = f"placeholder_{ad.id}.jpg"
            ad_image.image.save(
                filename,
                ContentFile(img_buffer.getvalue()),
                save=False
            )
            ad_image.save()
            
            self.stdout.write(f'Added image to: {ad.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added placeholder images to ads!'
            )
        )
