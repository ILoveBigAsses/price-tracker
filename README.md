# Trendyol Price Tracker / Trendyol Fiyat Takip Aracı

## Description / Açıklama
EN: A Python tool that monitors product prices on Trendyol and notifies you when they drop below a target value.  
TR: Trendyol’daki ürün fiyatlarını izleyen ve hedef fiyatın altına düşünce bilgilendiren Python aracıdır.

## Features / Özellikler
EN
- Fetch current price from Trendyol product pages
- Compare with target price
- Optional email notifications
- Save history to SQLite
- Optional Excel export or Flask dashboard

TR
- Trendyol ürün sayfalarından güncel fiyatı çeker
- Hedef fiyatla karşılaştırır
- İsteğe bağlı e-posta bildirimi
- Geçmişi SQLite veritabanına kaydeder
- İsteğe bağlı Excel çıktı veya Flask paneli

## Tech Stack / Teknolojiler
- Python 3.10+
- requests, BeautifulSoup
- sqlite3, openpyxl
- smtplib, email.mime
- python-dotenv

## Installation / Kurulum
EN
git clone https://github.com/<your_username>/price-tracker.git
cd price-tracker
pip install -r requirements.txt

TR
1) Depoyu klonla ve klasöre gir.  
2) Bağımlılıkları yükle: pip install -r requirements.txt

## Configuration / Yapılandırma
EN: Edit config.py and set:
- PRODUCTS: list of dicts with name, url, target_price
- Email settings if you want notifications

TR: config.py dosyasında düzenle:
- PRODUCTS: name, url, target_price alanları
- E-posta bildirimleri için gerekli ayarlar

Example / Örnek:
PRODUCTS = [
    {
        "name": "iPhone 17 Pro Max 256GB",
        "url": "https://www.trendyol.com/apple/iphone-17-pro-max-256gb-kozmik-turuncu-p-985256825",
        "target_price": 75000
    }
]

## Usage / Kullanım
EN
python scraper.py
Check console output or email if configured.

TR
python scraper.py
Sonuçları terminalde veya e-postada (ayarlandıysa) görürsün.

## Example Output / Örnek Çıktı
Price check started
Product: iPhone 17 Pro Max 256GB
Current price: 179999.00 TL
Target price: 75000.00 TL
Difference: 104999.00 TL

## Roadmap / Yol Haritası
- Add Flask web dashboard
- Multi-site support (Hepsiburada, Amazon TR)
- Telegram/Discord notifications

## License / Lisans
MIT License © 2025

## Author / Yazar
Goktug Ozkan  
Automation & Data Scraping Developer  
Email: drozkan2ægmail.com.
