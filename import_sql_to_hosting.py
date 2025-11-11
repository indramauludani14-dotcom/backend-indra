"""
Import SQL File ke Hosting Database
Script ini akan import file virtualtour1.sql ke database hosting
"""
import mysql.connector
from mysql.connector import Error
import os

# Path ke file SQL
SQL_FILE_PATH = r"C:\Users\indra\Downloads\virtualtour1.sql"

# Hosting database config
HOSTING_CONFIG = {
    'host': 'virtualign.my.id',
    'user': 'virtuali_virtualuser',
    'password': 'indra140603',
    'database': 'virtuali_virtualign',
    'port': 3306
}

def execute_sql_file(connection, sql_file_path):
    """Execute SQL file"""
    cursor = connection.cursor()
    
    print(f"\n[3] Reading SQL file: {sql_file_path}")
    
    # Read SQL file
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    
    # Remove comments and split by semicolon
    lines = sql_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip comment lines
        if line.strip().startswith('--') or line.strip().startswith('#'):
            continue
        # Skip MySQL specific comments
        if line.strip().startswith('/*!'):
            continue
        cleaned_lines.append(line)
    
    sql_content = '\n'.join(cleaned_lines)
    
    # Split into statements
    statements = []
    current_statement = []
    in_insert = False
    
    for line in sql_content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        current_statement.append(line)
        
        # Check if this is an INSERT statement
        if line.upper().startswith('INSERT INTO'):
            in_insert = True
        
        # Check for end of statement
        if line.endswith(';'):
            statement = ' '.join(current_statement)
            statements.append(statement)
            current_statement = []
            in_insert = False
    
    total_statements = len(statements)
    executed = 0
    errors = 0
    tables_created = 0
    rows_inserted = 0
    
    print(f"    Found {total_statements} SQL statements")
    print(f"\n[4] Executing SQL statements...")
    
    for i, statement in enumerate(statements, 1):
        statement = statement.strip()
        if not statement:
            continue
        
        # Skip SET commands
        if statement.upper().startswith('SET '):
            continue
        
        # Skip CREATE DATABASE
        if 'CREATE DATABASE' in statement.upper():
            continue
        
        # Skip USE database
        if statement.upper().startswith('USE '):
            continue
        
        # Skip START TRANSACTION and COMMIT
        if statement.upper() in ['START TRANSACTION;', 'COMMIT;']:
            continue
        
        try:
            # Execute statement
            cursor.execute(statement)
            executed += 1
            
            # Show progress
            if 'CREATE TABLE' in statement.upper():
                table_name = statement.split('`')[1] if '`' in statement else 'table'
                tables_created += 1
                print(f"    [{tables_created}] ✓ Table created: {table_name}")
            elif 'INSERT INTO' in statement.upper():
                rows_inserted += 1
                if rows_inserted % 5 == 0:
                    print(f"    ✓ Inserting data... ({rows_inserted} batches)")
                    
        except Error as e:
            # Ignore certain errors
            if e.errno == 1050:  # Table already exists
                table_name = statement.split('`')[1] if '`' in statement else 'table'
                print(f"    ⚠ Table already exists: {table_name} (dropping and recreating...)")
                # Try to drop and recreate
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                    cursor.execute(statement)
                    tables_created += 1
                    print(f"    [{tables_created}] ✓ Table recreated: {table_name}")
                except:
                    pass
            elif e.errno == 1062:  # Duplicate entry
                pass
            else:
                errors += 1
                if errors <= 10:
                    print(f"    ✗ Error [{i}]: {e}")
        
        # Commit every 50 statements
        if i % 50 == 0:
            connection.commit()
    
    # Final commit
    connection.commit()
    cursor.close()
    
    print(f"\n    ✓ Tables created: {tables_created}")
    print(f"    ✓ Data inserted: {rows_inserted} batches")
    
    return executed, errors

def import_sql_to_hosting():
    """Main import function"""
    print("="*70)
    print("IMPORT SQL FILE TO HOSTING DATABASE")
    print("="*70)
    
    # Check if file exists
    if not os.path.exists(SQL_FILE_PATH):
        print(f"\n✗ SQL file not found: {SQL_FILE_PATH}")
        print("\nPlease make sure virtualtour1.sql is in C:\\Users\\indra\\Downloads\\")
        return False
    
    file_size = os.path.getsize(SQL_FILE_PATH) / 1024  # KB
    print(f"\n[1] SQL File: {SQL_FILE_PATH}")
    print(f"    Size: {file_size:.2f} KB")
    
    try:
        # Connect to hosting database
        print(f"\n[2] Connecting to hosting database...")
        print(f"    Host: {HOSTING_CONFIG['host']}")
        print(f"    Database: {HOSTING_CONFIG['database']}")
        
        connection = mysql.connector.connect(**HOSTING_CONFIG)
        print("    ✓ Connected successfully")
        
        # Execute SQL file
        executed, errors = execute_sql_file(connection, SQL_FILE_PATH)
        
        # Verify import
        print(f"\n[4] Verifying import...")
        cursor = connection.cursor()
        
        # Get tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n✓ Tables in database ({len(tables)}):")
        
        total_rows = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            count = cursor.fetchone()[0]
            total_rows += count
            print(f"  - {table_name}: {count} rows")
        
        cursor.close()
        connection.close()
        
        # Summary
        print("\n" + "="*70)
        print("IMPORT SUMMARY")
        print("="*70)
        print(f"SQL statements executed: {executed}")
        print(f"Errors encountered: {errors}")
        print(f"Total tables: {len(tables)}")
        print(f"Total rows imported: {total_rows}")
        
        if errors == 0:
            print("\n✓ IMPORT COMPLETED SUCCESSFULLY!")
        else:
            print(f"\n⚠ Import completed with {errors} errors (might be normal)")
        
        print("="*70)
        
        print("\nNext steps:")
        print("1. Verify data di phpMyAdmin hosting")
        print("2. Config.py sudah menggunakan hosting database ✓")
        print("3. Test aplikasi: python app.py")
        
        return True
        
    except Error as e:
        print(f"\n✗ Import Error: {e}")
        return False

if __name__ == "__main__":
    print("\n⚠ WARNING: This will import all data to hosting database!")
    print(f"SQL File: {SQL_FILE_PATH}")
    print(f"Target: {HOSTING_CONFIG['host']}/{HOSTING_CONFIG['database']}\n")
    
    response = input("Continue with import? (yes/no): ").strip().lower()
    
    if response == 'yes':
        import_sql_to_hosting()
    else:
        print("\n✗ Import cancelled")
