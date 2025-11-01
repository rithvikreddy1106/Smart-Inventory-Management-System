import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_connection():
    """Create a database connection to MySQL database"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'inventory_system')
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def create_database():
    """Create a database if it doesn't exist"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'inventory_system')}")
        
        # Connect to the database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'inventory_system')
        )
        cursor = connection.cursor()
        
        # Create users table first (no dependencies)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20),
            user_type ENUM('customer', 'staff', 'admin') NOT NULL,
            is_approved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create categories table (no dependencies)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create suppliers table (no dependencies)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact_person VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create products table (depends on categories and suppliers)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            category_id INT,
            supplier_id INT,
            price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL DEFAULT 0,
            reorder_level INT DEFAULT 10,
            image_path VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
        )
        """)
        
        # Create orders table (depends on users)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
            total_amount DECIMAL(10, 2) NOT NULL,
            shipping_address TEXT,
            FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)
        
        # Create order_items table (depends on orders and products)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
        """)
        
        # Insert default admin user
        cursor.execute("""
        INSERT IGNORE INTO users (id, full_name, email, password, user_type, is_approved)
        VALUES (1, 'Admin User', 'admin@inventory.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', TRUE)
        """)
        
        # Insert sample categories
        cursor.execute("""
        INSERT IGNORE INTO categories (id, name, description) VALUES
        (1, 'Electronics', 'Electronic devices and accessories'),
        (2, 'Clothing', 'Apparel and fashion items'),
        (3, 'Food & Beverages', 'Food items and drinks'),
        (4, 'Books', 'Books and publications'),
        (5, 'Home & Garden', 'Home improvement and garden supplies')
        """)
        
        # Insert sample suppliers
        cursor.execute("""
        INSERT IGNORE INTO suppliers (id, name, contact_person, email, phone, address) VALUES
        (1, 'Tech Supplies Inc.', 'John Smith', 'john@techsupplies.com', '555-0101', '123 Tech Street, Silicon Valley, CA'),
        (2, 'Fashion Wholesale', 'Sarah Johnson', 'sarah@fashionwholesale.com', '555-0102', '456 Fashion Ave, New York, NY'),
        (3, 'Fresh Foods Co.', 'Mike Davis', 'mike@freshfoods.com', '555-0103', '789 Food Lane, Chicago, IL'),
        (4, 'Book Distributors', 'Emily Brown', 'emily@bookdist.com', '555-0104', '321 Book Blvd, Boston, MA'),
        (5, 'Home Essentials', 'David Wilson', 'david@homeessentials.com', '555-0105', '654 Home Road, Seattle, WA')
        """)
        
        # Insert sample products
        cursor.execute("""
        INSERT IGNORE INTO products (name, description, category_id, supplier_id, price, quantity, reorder_level) VALUES
        ('Laptop Computer', 'High-performance laptop with 16GB RAM', 1, 1, 999.99, 25, 5),
        ('Wireless Mouse', 'Ergonomic wireless mouse', 1, 1, 29.99, 50, 10),
        ('USB-C Cable', 'Fast charging USB-C cable', 1, 1, 12.99, 100, 20),
        ('Bluetooth Headphones', 'Noise-cancelling wireless headphones', 1, 1, 149.99, 30, 8),
        ('External Hard Drive', '1TB portable storage', 1, 1, 79.99, 40, 10),
        
        ('Men T-Shirt', 'Cotton casual t-shirt', 2, 2, 19.99, 75, 15),
        ('Women Jeans', 'Denim jeans - various sizes', 2, 2, 49.99, 60, 12),
        ('Sport Shoes', 'Running and training shoes', 2, 2, 89.99, 45, 10),
        ('Winter Jacket', 'Warm winter jacket', 2, 2, 129.99, 35, 8),
        ('Baseball Cap', 'Adjustable baseball cap', 2, 2, 15.99, 80, 15),
        
        ('Organic Coffee', 'Premium organic coffee beans - 1lb', 3, 3, 14.99, 120, 25),
        ('Green Tea', 'Organic green tea bags - 50 count', 3, 3, 9.99, 90, 20),
        ('Chocolate Bar', 'Dark chocolate bar - 100g', 3, 3, 3.99, 200, 40),
        ('Pasta', 'Italian pasta - 500g', 3, 3, 4.99, 150, 30),
        ('Olive Oil', 'Extra virgin olive oil - 1L', 3, 3, 12.99, 80, 15),
        
        ('Programming Book', 'Learn Python Programming', 4, 4, 39.99, 40, 10),
        ('Novel - Fiction', 'Bestselling fiction novel', 4, 4, 24.99, 55, 12),
        ('Cookbook', 'Healthy cooking recipes', 4, 4, 29.99, 35, 8),
        ('History Book', 'World history textbook', 4, 4, 44.99, 25, 5),
        ('Magazine', 'Monthly tech magazine', 4, 4, 5.99, 100, 20),
        
        ('LED Light Bulb', 'Energy efficient LED bulb', 5, 5, 8.99, 150, 30),
        ('Garden Hose', '50ft expandable garden hose', 5, 5, 34.99, 45, 10),
        ('Tool Set', 'Complete home tool kit', 5, 5, 79.99, 30, 8),
        ('Plant Pot', 'Ceramic plant pot - medium', 5, 5, 16.99, 70, 15),
        ('Cleaning Supplies', 'All-purpose cleaning kit', 5, 5, 24.99, 85, 18)
        """)
        
        connection.commit()
        print("Database and sample data created successfully")
        
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
