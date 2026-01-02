"""
Database Initialization Script
Run this file to create the database and sample data.
Usage: python db.py

This script:
1. Creates the database if it doesn't exist
2. Creates all required tables (users, categories, suppliers, products, orders, order_items)
3. Inserts sample data for testing

Note: Database connection details are configured in .env file or use defaults:
- DB_HOST=localhost
- DB_USER=root
- DB_PASSWORD= (empty by default)
- DB_NAME=inventory_system
"""
import db_config

if __name__ == "__main__":
    print("=" * 60)
    print("Smart Inventory Management System - Database Setup")
    print("=" * 60)
    print("\nCreating database and sample data...")
    print("This will:")
    print("  1. Create database 'inventory_system' if it doesn't exist")
    print("  2. Create all required tables")
    print("  3. Insert sample data (admin user, categories, suppliers, products)")
    print("\nPlease wait...\n")
    
    try:
        db_config.create_database()
        print("\n" + "=" * 60)
        print("Database setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run main.py to start the application.")
        print("\nDefault Admin Login:")
        print("  Email: admin@inventory.com")
        print("  Password: admin123")
        print("=" * 60)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("  1. MySQL server is running")
        print("  2. Database credentials in .env file are correct")
        print("  3. You have proper permissions to create databases")
