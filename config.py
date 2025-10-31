import os
from dotenv import load_dotenv

load_dotenv()

# Email ayarları
EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'your-email@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-app-password')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER', 'receiver@gmail.com')

# Veritabanı
DATABASE_PATH = 'prices.db'

# Kontrol sıklığı (dakika)
CHECK_INTERVAL = 60

# User agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# İzlenecek ürünler
PRODUCTS = [
    {
        'name': 'iPhone 17 Pro Max 256GB Kozmik Turuncu',
        'url': 'https://www.trendyol.com/apple/iphone-17-pro-max-256gb-kozmik-turuncu-p-985256825',
        'target_price': 75000
    }
]