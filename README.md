# Smart Inventory Management System (SIMS)

A comprehensive inventory management system built with Python, CustomTkinter, and MySQL.

## Features

### 🧍 Customer Features
- User registration and login
- Browse product catalog with search and category filters
- Add products to cart
- Place orders with shipping address
- View order history and status tracking

### 🧑‍💼 Staff Features
- Staff dashboard with key metrics
- Process pending orders (approve, ship, deliver, cancel)
- Manage inventory (add, edit, delete products)
- Low stock alerts and monitoring
- Real-time product search

### 🧑‍💻 Admin Features
- Admin dashboard with comprehensive statistics
- User management (approve staff, delete users)
- Supplier management (add, edit, delete suppliers)
- Detailed reports:
  - Sales reports with top products
  - Inventory reports with stock levels
  - Customer analytics with top customers
- Staff approval workflow

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- MySQL Workbench (optional, for database management)

## Installation

### 1. Install MySQL

Download and install MySQL from [mysql.com](https://dev.mysql.com/downloads/mysql/)

During installation:
- Set root password (or leave empty)
- Start MySQL Server
- Note the port (default: 3306)

### 2. Clone or Download the Project

```bash
cd path/to/Inventory-Management-System-main
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database Connection

Edit the `.env` file in the project root:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_system
```

**Note:** If you didn't set a MySQL root password, leave `DB_PASSWORD` empty.

### 5. Initialize the Database

Run the database initialization script:

```bash
python db_config.py
```

This will:
- Create the `inventory_system` database
- Create all required tables
- Insert sample data (categories, suppliers, products)
- Create default admin account

## Default Login Credentials

### Admin Account
- **Email:** admin@inventory.com
- **Password:** admin123

### Test the System
1. Register as a Customer or Staff member
2. Staff members require admin approval before login
3. Customers can login immediately after registration

## Running the Application

```bash
python main.py
```

## Database Schema

The system uses the following tables:
- `users` - Customer, Staff, and Admin accounts
- `categories` - Product categories
- `suppliers` - Supplier information
- `products` - Product inventory
- `orders` - Customer orders
- `order_items` - Order line items

## Sample Data

The system includes sample data:
- **5 Categories:** Electronics, Clothing, Food & Beverages, Books, Home & Garden
- **5 Suppliers:** Tech Supplies Inc., Fashion Wholesale, Fresh Foods Co., Book Distributors, Home Essentials
- **25 Products:** Various items across all categories
- **1 Admin User:** admin@inventory.com / admin123

## User Workflow

### Customer Workflow
1. Register as a customer
2. Login
3. Browse products (use search and category filters)
4. Add products to cart
5. Place order with shipping address
6. View order history

### Staff Workflow
1. Register as staff member
2. Wait for admin approval
3. Login after approval
4. View dashboard with pending orders and low stock alerts
5. Process pending orders
6. Manage inventory (add/edit/delete products)
7. Check low stock alerts

### Admin Workflow
1. Login with admin credentials
2. View comprehensive dashboard
3. Approve pending staff registrations
4. Manage users (view, delete)
5. Manage suppliers (add, edit, delete)
6. View detailed reports

## Troubleshooting

### MySQL Connection Error
- Verify MySQL is running
- Check `.env` file credentials
- Ensure the database user has proper permissions

### Module Not Found Error
```bash
pip install --upgrade -r requirements.txt
```

### Database Already Exists
The initialization script is safe to run multiple times. It will skip existing tables and use `INSERT IGNORE` for sample data.

### Permission Denied
Make sure your MySQL user has the following permissions:
```sql
GRANT ALL PRIVILEGES ON inventory_system.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Project Structure

```
Inventory-Management-System/
├── main.py              # Application entry point
├── auth.py              # Login and registration
├── customer.py          # Customer dashboard
├── staff.py             # Staff dashboard
├── admin.py             # Admin dashboard
├── db_config.py         # Database configuration and initialization
├── requirements.txt     # Python dependencies
├── .env                 # Database configuration
├── images/              # UI images and logos
└── README.md           # This file
```

## Technologies Used

- **Python 3.x** - Core programming language
- **CustomTkinter** - Modern UI framework
- **MySQL** - Database management system
- **Pillow** - Image processing
- **python-dotenv** - Environment variable management

## Features Implemented

✅ User authentication with role-based access
✅ Staff approval workflow
✅ Product catalog with search and filters
✅ Shopping cart functionality
✅ Order management system
✅ Inventory management
✅ Low stock alerts
✅ Comprehensive reporting
✅ Supplier management
✅ User management
✅ Sample data included

## Security Notes

- Passwords are hashed using SHA-256
- Role-based access control (Customer, Staff, Admin)
- Staff members require admin approval
- Admin users cannot be deleted
- SQL injection prevention using parameterized queries

## Support

For issues or questions:
- Check the Troubleshooting section
- Review the database logs
- Verify all dependencies are installed
- Ensure MySQL is running

## License

This project is created for educational purposes.

## Credits

Developed as part of the Information Systems Capstone Project.
