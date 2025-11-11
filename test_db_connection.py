"""
Test Database Connection
Untuk mengecek apakah bisa connect ke database hosting
"""
import mysql.connector
from mysql.connector import Error
import sys

def test_connection_hosting():
    """Test connection ke hosting database"""
    print("="*60)
    print("Testing Connection to HOSTING Database")
    print("="*60)
    
    config = {
        'host': 'virtualign.my.id',
        'database': 'virtuali_virtualign',
        'user': 'virtuali_virtualuser',
        'password': 'indra140603',
        'port': 3306,
        'connection_timeout': 10
    }
    
    try:
        print(f"\nConnecting to:")
        print(f"  Host    : {config['host']}")
        print(f"  Database: {config['database']}")
        print(f"  User    : {config['user']}")
        print(f"  Port    : {config['port']}")
        print("\nAttempting connection...")
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"\n✓ SUCCESS: Connected to MySQL Server")
            print(f"  Version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"  Database: {record[0]}")
            
            # Test query
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"\n✓ Tables found: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            connection.close()
            print("\n✓ Connection closed successfully")
            return True
            
    except Error as e:
        print(f"\n✗ FAILED: Cannot connect to MySQL")
        print(f"  Error Code: {e.errno}")
        print(f"  Error: {e.msg}")
        
        if e.errno == 1130:
            print("\n" + "="*60)
            print("SOLUSI:")
            print("="*60)
            print("IP Anda tidak di-whitelist di hosting MySQL.")
            print("\nLangkah-langkah:")
            print("1. Login ke cPanel: https://virtualign.my.id:2083")
            print("2. Cari menu 'Remote MySQL'")
            print("3. Tambahkan IP Anda ke Access Hosts")
            print("4. Atau hubungi support hosting")
            print("\nAtau gunakan database lokal untuk development:")
            print("  DB_HOST = 'localhost'")
            print("  DB_USER = 'root'")
            print("  DB_PASSWORD = ''")
            print("  DB_NAME = 'virtualtour1'")
        
        return False

def test_connection_local():
    """Test connection ke local database (Laragon)"""
    print("\n" + "="*60)
    print("Testing Connection to LOCAL Database (Laragon)")
    print("="*60)
    
    config = {
        'host': 'localhost',
        'database': 'virtualtour1',
        'user': 'root',
        'password': '',
        'port': 3306,
        'connection_timeout': 5
    }
    
    try:
        print(f"\nConnecting to:")
        print(f"  Host    : {config['host']}")
        print(f"  Database: {config['database']}")
        print(f"  User    : {config['user']}")
        print(f"  Port    : {config['port']}")
        print("\nAttempting connection...")
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"\n✓ SUCCESS: Connected to MySQL Server")
            print(f"  Version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"  Database: {record[0]}")
            
            # Test query
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"\n✓ Tables found: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            connection.close()
            print("\n✓ Connection closed successfully")
            return True
            
    except Error as e:
        print(f"\n✗ FAILED: Cannot connect to MySQL")
        print(f"  Error: {e}")
        print("\nPastikan Laragon MySQL sudah running!")
        return False

def get_my_ip():
    """Get public IP address"""
    try:
        import requests
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return "Cannot detect"

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DATABASE CONNECTION TESTER")
    print("="*60)
    
    # Get IP
    my_ip = get_my_ip()
    print(f"\nYour Public IP: {my_ip}")
    print("(This IP needs to be whitelisted in hosting Remote MySQL)")
    
    # Test hosting connection
    hosting_ok = test_connection_hosting()
    
    # Test local connection
    local_ok = test_connection_local()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Hosting Database (virtualign.my.id): {'✓ OK' if hosting_ok else '✗ FAILED'}")
    print(f"Local Database (localhost):          {'✓ OK' if local_ok else '✗ FAILED'}")
    
    print("\n" + "="*60)
    print("RECOMMENDATION")
    print("="*60)
    
    if hosting_ok:
        print("✓ Gunakan hosting database - sudah bisa connect!")
        print("  Update config.py dengan hosting credentials")
    elif local_ok:
        print("⚠ Gunakan local database untuk development")
        print("  Hosting database tidak bisa diakses dari IP Anda")
        print("  Solusi: Whitelist IP di cPanel Remote MySQL")
    else:
        print("✗ Tidak ada database yang bisa digunakan!")
        print("  1. Start Laragon MySQL untuk local development")
        print("  2. Atau setup Remote MySQL di hosting")
    
    print("="*60 + "\n")
