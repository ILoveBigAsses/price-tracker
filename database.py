import sqlite3
from datetime import datetime
import config

def init_database():
    """Veritabanını oluştur"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_url TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_price(product_name, product_url, price):
    """Fiyat kaydı ekle"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO prices (product_name, product_url, price)
        VALUES (?, ?, ?)
    ''', (product_name, product_url, price))
    
    conn.commit()
    conn.close()

def get_price_history(product_name, limit=30):
    """Ürünün fiyat geçmişini getir"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT price, timestamp 
        FROM prices 
        WHERE product_name = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (product_name, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_all_products():
    """Tüm ürünleri getir"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT product_name, product_url 
        FROM prices
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_latest_prices():
    """Her ürün için en son fiyatı getir"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p1.product_name, p1.price, p1.timestamp
        FROM prices p1
        INNER JOIN (
            SELECT product_name, MAX(timestamp) as max_time
            FROM prices
            GROUP BY product_name
        ) p2 ON p1.product_name = p2.product_name 
        AND p1.timestamp = p2.max_time
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results