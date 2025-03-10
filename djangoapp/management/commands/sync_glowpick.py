# myapp/management/commands/sync_glowpick.py

import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from django.core.management.base import BaseCommand
from myapp.models import Product  # or wherever your Product model is

class Command(BaseCommand):
    help = 'Scrapes data from Glowpick and syncs to the local database.'

    def handle(self, *args, **options):
        self.stdout.write("Starting Glowpick sync...")

        # 1) Scrape
        product_data = self.scrape_glowpick_products()

        # 2) Translate (optional)
        product_data = self.translate_product_data(product_data)

        # 3) Upsert into DB
        self.upsert_products(product_data)

        self.stdout.write("Glowpick sync complete.")

    def scrape_glowpick_products(self):
        url = "https://www.glowpick.com/categories/1?tab=ranking&order=reviewCount_desc"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_cards = soup.select('.product-card')  # Example: adapt to actual selectors
        product_data_list = []
        for card in product_cards:
            name = card.select_one('.product-name').get_text(strip=True)
            brand = card.select_one('.product-brand').get_text(strip=True)
            # Parse other fields as needed

            product_data_list.append({
                'name': name,
                'brand': brand,
                # ...
            })

        return product_data_list

    def translate_product_data(self, product_data_list):
        translator = Translator()
        for product in product_data_list:
            product['name_en'] = translator.translate(product['name'], dest='en').text
            product['brand_en'] = translator.translate(product['brand'], dest='en').text
        return product_data_list

    def upsert_products(self, product_data_list):
        for p_data in product_data_list:
            # Example upsert logic:
            # Try to find existing by (name, brand) or some unique ID
            obj, created = Product.objects.update_or_create(
                name=p_data['name'],
                brand=p_data['brand'],
                defaults={
                    'name_en': p_data.get('name_en'),
                    'brand_en': p_data.get('brand_en'),
                    # ...
                }
            )
            if created:
                self.stdout.write(f"Created new product: {obj.name}")
            else:
                self.stdout.write(f"Updated product: {obj.name}")

# Usage:
# python manage.py sync_glowpick

