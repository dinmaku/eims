#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from eims_admin_project.eims_admin_backend.app.db import get_db_connection

def check_availability_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'supplier_availability'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        print(f"Table exists: {table_exists}")
        
        if table_exists:
            # Check table structure
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'supplier_availability'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print("Table structure:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
            
            # Check if there's any data
            cursor.execute("SELECT COUNT(*) FROM supplier_availability")
            count = cursor.fetchone()[0]
            print(f"Total records: {count}")
            
            if count > 0:
                # Show some sample data
                cursor.execute("SELECT * FROM supplier_availability LIMIT 5")
                records = cursor.fetchall()
                print("Sample data:")
                for record in records:
                    print(f"  {record}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error checking table: {e}")

if __name__ == "__main__":
    check_availability_table() 