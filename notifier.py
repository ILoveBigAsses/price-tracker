import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_price_alert(product_name, current_price, target_price, product_url):
    """Fiyat düşünce email gönder"""
    
    subject = f"🎉 {product_name} - Hedef Fiyata Ulaşıldı!"
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #2ecc71;">Fiyat Düştü! 🎉</h2>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>{product_name}</h3>
            <p style="font-size: 18px;">
                <strong>Güncel Fiyat:</strong> 
                <span style="color: #e74c3c; font-size: 24px;">{current_price:,.2f} TL</span>
            </p>
            <p style="font-size: 16px;">
                <strong>Hedef Fiyat:</strong> {target_price:,.2f} TL
            </p>
            <p style="font-size: 16px;">
                <strong>İndirim:</strong> 
                <span style="color: #2ecc71;">{target_price - current_price:,.2f} TL tasarruf!</span>
            </p>
        </div>
        
        <a href="{product_url}" 
           style="background: #3498db; color: white; padding: 15px 30px; 
                  text-decoration: none; border-radius: 5px; display: inline-block;">
            Ürünü Görüntüle
        </a>
        
        <p style="margin-top: 30px; color: #7f8c8d; font-size: 12px;">
            Bu bildirim Price Tracker tarafından otomatik olarak gönderilmiştir.
        </p>
    </body>
    </html>
    """
    
    try:
        # Email oluştur
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = config.EMAIL_RECEIVER
        
        # HTML içerik ekle
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        # Gmail SMTP ile gönder
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email gönderildi: {config.EMAIL_RECEIVER}")
        return True
        
    except Exception as e:
        print(f"❌ Email gönderilemedi: {e}")
        return False

def send_daily_report():
    """Günlük rapor gönder"""
    from database import get_latest_prices
    
    prices = get_latest_prices()
    
    if not prices:
        print("📭 Rapor için veri yok")
        return
    
    subject = "📊 Günlük Fiyat Raporu"
    
    body = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>📊 Günlük Fiyat Raporu</h2>
        <table style="border-collapse: collapse; width: 100%;">
            <tr style="background: #3498db; color: white;">
                <th style="padding: 10px; border: 1px solid #ddd;">Ürün</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Fiyat</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Tarih</th>
            </tr>
    """
    
    for product_name, price, timestamp in prices:
        body += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{product_name}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{price:,.2f} TL</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{timestamp}</td>
            </tr>
        """
    
    body += """
        </table>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_SENDER
        msg['To'] = config.EMAIL_RECEIVER
        
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Günlük rapor gönderildi")
        return True
        
    except Exception as e:
        print(f"❌ Rapor gönderilemedi: {e}")
        return False