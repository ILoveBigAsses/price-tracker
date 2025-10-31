import requests
from bs4 import BeautifulSoup
import re
import time
import json
import config
import database
from notifier import send_price_alert

def get_trendyol_price_html(url):
    """HTML parse ederek fiyat al"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }
    
    try:
        print(f"🌐 Sayfa indiriliyor...")
        
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"✅ Sayfa alındı (Status: {response.status_code})")
        
        # HTML'i dosyaya kaydet debug için
        with open('trendyol_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("📝 HTML 'trendyol_page.html' dosyasına kaydedildi")
        
        # JSON içinde fiyat ara (Trendyol sayfada JSON gömer)
        json_pattern = r'<script[^>]*>window\.__PRODUCT_DETAIL_APP_INITIAL_STATE__\s*=\s*({.*?})</script>'
        json_match = re.search(json_pattern, response.text, re.DOTALL)
        
        if json_match:
            print("✅ JSON verisi bulundu, parse ediliyor...")
            json_str = json_match.group(1)
            data = json.loads(json_str)
            
            # JSON'u dosyaya kaydet
            with open('trendyol_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("📝 JSON 'trendyol_data.json' dosyasına kaydedildi")
            
            # Fiyatı JSON'dan çıkar
            if 'product' in data:
                product = data['product']
                price = product.get('price', {}).get('discountedPrice') or product.get('price', {}).get('sellingPrice')
                
                if price:
                    print(f"✅ Fiyat JSON'dan alındı: {price} TL")
                    return float(price)
        
        # JSON bulunamazsa HTML parse et
        print("⚠️ JSON bulunamadı, HTML parse ediliyor...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tüm script taglerini kontrol et
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'price' in script.string.lower():
                # Fiyat içeren script'i bul
                price_match = re.search(r'"(?:discountedPrice|sellingPrice)"\s*:\s*(\d+(?:\.\d+)?)', script.string)
                if price_match:
                    price = float(price_match.group(1))
                    print(f"✅ Fiyat script'ten alındı: {price} TL")
                    return price
        
        # Son çare: Tüm sayıları ara ve en büyük olanı al (fiyat genelde büyük sayıdır)
        print("⚠️ Script'te bulunamadı, sayıları tarıyor...")
        all_numbers = re.findall(r'\b(\d{4,6}(?:[.,]\d{2})?)\b', response.text)
        if all_numbers:
            # Virgül/nokta formatını düzelt ve sayıya çevir
            prices = []
            for num in all_numbers:
                num_clean = num.replace(',', '.').replace('.', '', num.count('.') - 1)
                try:
                    prices.append(float(num_clean))
                except:
                    pass
            
            if prices:
                # 10000-200000 TL arası olan en büyük sayı muhtemelen fiyattır
                valid_prices = [p for p in prices if 10000 <= p <= 200000]
                if valid_prices:
                    price = max(valid_prices)
                    print(f"⚠️ Tahmini fiyat bulundu: {price} TL (Doğruluğu kontrol et!)")
                    return price
        
        print("❌ Hiçbir yöntemle fiyat bulunamadı")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ İstek hatası: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse hatası: {e}")
        return None
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_all_products():
    """Tüm ürünleri kontrol et"""
    print(f"\n{'='*60}")
    print(f"🔍 Fiyat kontrolü başladı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    for product in config.PRODUCTS:
        name = product['name']
        url = product['url']
        target_price = product['target_price']
        
        print(f"\n📦 Kontrol ediliyor: {name}")
        print(f"🔗 URL: {url}")
        print(f"🎯 Hedef fiyat: {target_price:,.2f} TL")
        
        current_price = get_trendyol_price_html(url)
        
        if current_price:
            print(f"💰 Güncel fiyat: {current_price:,.2f} TL")
            
            # Veritabanına kaydet
            database.save_price(name, url, current_price)
            
            # Hedef fiyatın altındaysa bildirim gönder
            if current_price <= target_price:
                print(f"🎉 Hedef fiyata ulaşıldı! ({target_price:,.2f} TL)")
                send_price_alert(name, current_price, target_price, url)
            else:
                diff = current_price - target_price
                print(f"⏳ Hedef fiyata {diff:,.2f} TL kaldı")
        else:
            print(f"❌ Fiyat alınamadı: {name}")
            print(f"💡 'trendyol_page.html' ve 'trendyol_data.json' dosyalarını kontrol et")
        
        # Rate limiting
        print(f"\n⏱️  2 saniye bekleniyor...")
        time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"✅ Kontrol tamamlandı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    database.init_database()
    check_all_products()