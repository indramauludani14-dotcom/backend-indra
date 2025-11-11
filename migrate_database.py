"""
Export Database dari Laragon dan Import ke Hosting
Script ini akan:
1. Membaca semua data dari database lokal (virtualtour1)
2. Menulis ke database hosting (virtuali_virtualign)
"""
import mysql.connector
from mysql.connector import Error

# Konfigurasi database
LOCAL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'virtualtour1',
    'port': 3306
}

HOSTING_CONFIG = {
    'host': 'virtualign.my.id',
    'user': 'virtuali_virtualuser',
    'password': 'indra140603',
    'database': 'virtuali_virtualign',
    'port': 3306
}

def get_table_structure(cursor, table_name):
    """Get CREATE TABLE statement"""
    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
    result = cursor.fetchone()
    return result[1] if result else None

def copy_table(source_conn, dest_conn, table_name):
    """Copy table structure and data from source to destination"""
    source_cursor = source_conn.cursor()
    dest_cursor = dest_conn.cursor()
    
    try:
        # Get table structure
        print(f"\n  Copying table: {table_name}")
        create_sql = get_table_structure(source_cursor, table_name)
        
        if not create_sql:
            print(f"    ✗ Could not get structure for {table_name}")
            return False
        
        # Drop table if exists in destination
        dest_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        
        # Create table in destination
        dest_cursor.execute(create_sql)
        print(f"    ✓ Table structure created")
        
        # Get data from source
        source_cursor.execute(f"SELECT * FROM `{table_name}`")
        rows = source_cursor.fetchall()
        
        if not rows:
            print(f"    ⚠ No data to copy (0 rows)")
            return True
        
        # Get column names
        columns = [desc[0] for desc in source_cursor.description]
        
        # Insert data to destination
        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f"INSERT INTO `{table_name}` ({', '.join(['`' + col + '`' for col in columns])}) VALUES ({placeholders})"
        
        dest_cursor.executemany(insert_sql, rows)
        dest_conn.commit()
        
        print(f"    ✓ Copied {len(rows)} rows")
        return True
        
    except Error as e:
        print(f"    ✗ Error copying {table_name}: {e}")
        return False
    finally:
        source_cursor.close()
        dest_cursor.close()

def migrate_database():
    """Main migration function"""
    print("="*70)
    print("DATABASE MIGRATION: Laragon → Hosting")
    print("="*70)
    
    source_conn = None
    dest_conn = None
    
    try:
        # Connect to source (local)
        print("\n[1] Connecting to LOCAL database (Laragon)...")
        print(f"    Host: {LOCAL_CONFIG['host']}")
        print(f"    Database: {LOCAL_CONFIG['database']}")
        
        source_conn = mysql.connector.connect(**LOCAL_CONFIG)
        print("    ✓ Connected to local database")
        
        # Connect to destination (hosting)
        print("\n[2] Connecting to HOSTING database...")
        print(f"    Host: {HOSTING_CONFIG['host']}")
        print(f"    Database: {HOSTING_CONFIG['database']}")
        
        dest_conn = mysql.connector.connect(**HOSTING_CONFIG)
        print("    ✓ Connected to hosting database")
        
        # Get list of tables from source
        print("\n[3] Getting table list from local database...")
        source_cursor = source_conn.cursor()
        source_cursor.execute("SHOW TABLES")
        tables = [table[0] for table in source_cursor.fetchall()]
        source_cursor.close()
        
        print(f"    Found {len(tables)} tables:")
        for table in tables:
            print(f"      - {table}")
        
        # Copy each table
        print("\n[4] Copying tables...")
        success_count = 0
        failed_tables = []
        
        for i, table in enumerate(tables, 1):
            print(f"\n  [{i}/{len(tables)}] Processing: {table}")
            if copy_table(source_conn, dest_conn, table):
                success_count += 1
            else:
                failed_tables.append(table)
        
        # Summary
        print("\n" + "="*70)
        print("MIGRATION SUMMARY")
        print("="*70)
        print(f"Total tables: {len(tables)}")
        print(f"Successfully copied: {success_count}")
        print(f"Failed: {len(failed_tables)}")
        
        if failed_tables:
            print(f"\nFailed tables:")
            for table in failed_tables:
                print(f"  - {table}")
        
        # Verify destination
        print("\n" + "="*70)
        print("VERIFICATION - Hosting Database")
        print("="*70)
        
        dest_cursor = dest_conn.cursor()
        dest_cursor.execute("SHOW TABLES")
        dest_tables = dest_cursor.fetchall()
        
        print(f"\nTables in hosting database ({len(dest_tables)}):")
        for table in dest_tables:
            dest_cursor.execute(f"SELECT COUNT(*) FROM `{table[0]}`")
            count = dest_cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} rows")
        
        dest_cursor.close()
        
        print("\n" + "="*70)
        if success_count == len(tables):
            print("✓ MIGRATION COMPLETED SUCCESSFULLY!")
        else:
            print("⚠ MIGRATION COMPLETED WITH ERRORS")
        print("="*70)
        
        print("\nNext steps:")
        print("1. Verify data di phpMyAdmin hosting")
        print("2. Update config.py sudah benar (hosting)")
        print("3. Test aplikasi: python app.py")
        
        return success_count == len(tables)
        
    except Error as e:
        print(f"\n✗ Migration Error: {e}")
        return False
        
    finally:
        if source_conn and source_conn.is_connected():
            source_conn.close()
            print("\n✓ Local connection closed")
        
        if dest_conn and dest_conn.is_connected():
            dest_conn.close()
            print("✓ Hosting connection closed")

if __name__ == "__main__":
    print("\n⚠ WARNING: This will OVERWRITE all data in hosting database!")
    print("Make sure you have a backup before proceeding.\n")
    
    response = input("Continue with migration? (yes/no): ").strip().lower()
    
    if response == 'yes':
        migrate_database()
    else:
        print("\n✗ Migration cancelled")
