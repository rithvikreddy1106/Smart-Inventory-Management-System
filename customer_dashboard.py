import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from mysql.connector import Error
import db_config
from datetime import datetime

class CustomerDashboard:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.cart = []  # List of {product_id, name, price, quantity}
        
        # Create main container
        self.container = ctk.CTkFrame(parent)
        self.container.pack(fill="both", expand=True)
        
        # Create header
        self.create_header()
        
        # Create navigation
        self.create_navigation()
        
        # Create content area
        self.content_frame = ctk.CTkFrame(self.container)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Show product catalog by default
        self.show_products()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.container, height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            header_frame,
            text=f"Welcome, {self.main_app.current_user['full_name']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        welcome_label.pack(side="left", padx=20)
        
        # Cart button
        self.cart_button = ctk.CTkButton(
            header_frame,
            text=f"🛒 Cart ({len(self.cart)})",
            font=ctk.CTkFont(size=14),
            width=120,
            command=self.show_cart
        )
        self.cart_button.pack(side="right", padx=20)
        
        # Logout button
        logout_button = ctk.CTkButton(
            header_frame,
            text="Logout",
            font=ctk.CTkFont(size=14),
            width=100,
            command=self.logout
        )
        logout_button.pack(side="right", padx=5)
    
    def create_navigation(self):
        nav_frame = ctk.CTkFrame(self.container, height=50)
        nav_frame.pack(fill="x", padx=10, pady=5)
        nav_frame.pack_propagate(False)
        
        # Navigation buttons
        products_btn = ctk.CTkButton(
            nav_frame,
            text="Browse Products",
            font=ctk.CTkFont(size=14),
            width=150,
            command=self.show_products
        )
        products_btn.pack(side="left", padx=10)
        
        orders_btn = ctk.CTkButton(
            nav_frame,
            text="My Orders",
            font=ctk.CTkFont(size=14),
            width=150,
            command=self.show_orders
        )
        orders_btn.pack(side="left", padx=10)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_products(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Product Catalog",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Search and filter frame
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Search:", font=ctk.CTkFont(size=14))
        search_label.pack(side="left", padx=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Search products...")
        self.search_entry.pack(side="left", padx=10)
        
        search_button = ctk.CTkButton(search_frame, text="Search", width=100, command=self.load_products)
        search_button.pack(side="left", padx=10)
        
        # Category filter
        category_label = ctk.CTkLabel(search_frame, text="Category:", font=ctk.CTkFont(size=14))
        category_label.pack(side="left", padx=10)
        
        self.category_var = tk.StringVar(value="All")
        categories = self.get_categories()
        category_menu = ctk.CTkOptionMenu(
            search_frame,
            variable=self.category_var,
            values=["All"] + categories,
            width=150,
            command=lambda x: self.load_products()
        )
        category_menu.pack(side="left", padx=10)
        
        # Products frame with scrollbar and dynamic grid
        products_container = ctk.CTkFrame(self.content_frame)
        products_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(products_container, bg=self.content_frame.cget("fg_color")[1])
        scrollbar = ctk.CTkScrollbar(products_container, command=canvas.yview)
        self.products_frame = ctk.CTkFrame(canvas)
        
        # Store canvas reference
        self.products_canvas = canvas
        self.products_container = products_container
        
        def update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.products_frame.bind("<Configure>", update_scrollregion)
        
        def update_canvas_width(event=None):
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:
                canvas_window = canvas.find_all()
                if canvas_window:
                    canvas.itemconfig(canvas_window[0], width=canvas_width)
        
        canvas.create_window((0, 0), window=self.products_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind("<Configure>", update_canvas_width)
        
        # Load products
        self.load_products()
    
    def get_categories(self):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM categories ORDER BY name")
                categories = [row[0] for row in cursor.fetchall()]
                cursor.close()
                connection.close()
                return categories
        except Error as e:
            print(f"Error: {e}")
        return []
    
    def load_products(self):
        # Clear products frame
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Build query
                query = """
                    SELECT p.*, c.name as category_name 
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.id
                    WHERE p.quantity > 0
                """
                params = []
                
                # Add search filter
                search_term = self.search_entry.get().strip()
                if search_term:
                    query += " AND (p.name LIKE %s OR p.description LIKE %s)"
                    params.extend([f"%{search_term}%", f"%{search_term}%"])
                
                # Add category filter
                if self.category_var.get() != "All":
                    query += " AND c.name = %s"
                    params.append(self.category_var.get())
                
                query += " ORDER BY p.name"
                
                cursor.execute(query, params)
                products = cursor.fetchall()
                
                if not products:
                    no_products_label = ctk.CTkLabel(
                        self.products_frame,
                        text="No products found",
                        font=ctk.CTkFont(size=16)
                    )
                    no_products_label.pack(pady=50)
                else:
                    # Calculate dynamic columns based on available width
                    # Get actual available width
                    self.products_container.update_idletasks()
                    self.products_canvas.update_idletasks()
                    
                    try:
                        container_width = self.products_container.winfo_width()
                        if container_width < 100:
                            container_width = self.content_frame.winfo_width() - 60  # Account for padding and scrollbar
                        if container_width < 100:
                            container_width = self.main_app.winfo_width() - 200
                        if container_width < 100:
                            container_width = 1200  # Fallback
                        
                        # Card width: 250px card + 20px padding (10px each side)
                        card_width = 270
                        num_columns = max(2, int(container_width / card_width))
                        num_columns = min(num_columns, 8)  # Max 8 columns
                    except Exception as e:
                        print(f"Error calculating columns: {e}")
                        num_columns = 4  # Default fallback
                    
                    # Configure grid columns for dynamic layout
                    for i in range(num_columns):
                        self.products_frame.grid_columnconfigure(i, weight=1, uniform="product_cols")
                    
                    # Display products in dynamic grid
                    row = 0
                    col = 0
                    for product in products:
                        product_card = self.create_product_card(product)
                        product_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                        
                        col += 1
                        if col >= num_columns:
                            col = 0
                            row += 1
                    
                    # Update canvas window width to match container
                    self.products_canvas.update_idletasks()
                    canvas_width = self.products_canvas.winfo_width()
                    if canvas_width > 1:
                        canvas_items = self.products_canvas.find_all()
                        if canvas_items:
                            self.products_canvas.itemconfig(canvas_items[0], width=canvas_width)
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")
    
    def create_product_card(self, product):
        card = ctk.CTkFrame(self.products_frame, width=250, height=300)
        card.pack_propagate(False)
        
        # Product name
        name_label = ctk.CTkLabel(
            card,
            text=product['name'],
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=230
        )
        name_label.pack(pady=(10, 5))
        
        # Category
        category_label = ctk.CTkLabel(
            card,
            text=f"Category: {product['category_name'] or 'N/A'}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        category_label.pack(pady=2)
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=product['description'] or 'No description',
            font=ctk.CTkFont(size=11),
            wraplength=230,
            text_color="gray"
        )
        desc_label.pack(pady=5)
        
        # Price
        price_label = ctk.CTkLabel(
            card,
            text=f"${product['price']:.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="green"
        )
        price_label.pack(pady=5)
        
        # Stock
        stock_label = ctk.CTkLabel(
            card,
            text=f"In Stock: {product['quantity']}",
            font=ctk.CTkFont(size=12)
        )
        stock_label.pack(pady=2)
        
        # Quantity selector
        qty_frame = ctk.CTkFrame(card, fg_color="transparent")
        qty_frame.pack(pady=10)
        
        qty_label = ctk.CTkLabel(qty_frame, text="Qty:", font=ctk.CTkFont(size=12))
        qty_label.pack(side="left", padx=5)
        
        qty_spinbox = ctk.CTkEntry(qty_frame, width=60)
        qty_spinbox.insert(0, "1")
        qty_spinbox.pack(side="left", padx=5)
        
        # Add to cart button
        add_button = ctk.CTkButton(
            card,
            text="Add to Cart",
            width=200,
            command=lambda: self.add_to_cart(product, qty_spinbox)
        )
        add_button.pack(pady=10)
        
        return card
    
    def add_to_cart(self, product, qty_entry):
        # Validate quantity input
        qty_text = qty_entry.get().strip()
        if not qty_text:
            messagebox.showerror("Error", "Please enter a quantity")
            qty_entry.delete(0, "end")
            qty_entry.insert(0, "1")
            return
        
        try:
            quantity = int(qty_text)
            if quantity < 1:
                messagebox.showerror("Error", "Quantity must be at least 1")
                qty_entry.delete(0, "end")
                qty_entry.insert(0, "1")
                return
            if quantity > product['quantity']:
                messagebox.showerror("Error", f"Only {product['quantity']} items available in stock")
                qty_entry.delete(0, "end")
                qty_entry.insert(0, str(product['quantity']))
                return
            
            # Check if product already in cart
            for item in self.cart:
                if item['product_id'] == product['id']:
                    item['quantity'] += quantity
                    messagebox.showinfo("Success", f"Updated {product['name']} quantity in cart")
                    self.update_cart_button()
                    return
            
            # Add new item to cart
            self.cart.append({
                'product_id': product['id'],
                'name': product['name'],
                'price': float(product['price']),
                'quantity': quantity,
                'available_stock': product['quantity']
            })
            
            messagebox.showinfo("Success", f"Added {product['name']} to cart")
            self.update_cart_button()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
    
    def update_cart_button(self):
        self.cart_button.configure(text=f"🛒 Cart ({len(self.cart)})")
    
    def show_cart(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Shopping Cart",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        if not self.cart:
            empty_label = ctk.CTkLabel(
                self.content_frame,
                text="Your cart is empty",
                font=ctk.CTkFont(size=16)
            )
            empty_label.pack(pady=50)
            
            back_button = ctk.CTkButton(
                self.content_frame,
                text="Continue Shopping",
                width=200,
                command=self.show_products
            )
            back_button.pack(pady=20)
            return
        
        # Cart items frame
        cart_frame = ctk.CTkFrame(self.content_frame)
        cart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(cart_frame)
        headers_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(headers_frame, text="Product", font=ctk.CTkFont(size=14, weight="bold"), width=200).pack(side="left", padx=10)
        ctk.CTkLabel(headers_frame, text="Price", font=ctk.CTkFont(size=14, weight="bold"), width=100).pack(side="left", padx=10)
        ctk.CTkLabel(headers_frame, text="Quantity", font=ctk.CTkFont(size=14, weight="bold"), width=100).pack(side="left", padx=10)
        ctk.CTkLabel(headers_frame, text="Total", font=ctk.CTkFont(size=14, weight="bold"), width=100).pack(side="left", padx=10)
        ctk.CTkLabel(headers_frame, text="Action", font=ctk.CTkFont(size=14, weight="bold"), width=100).pack(side="left", padx=10)
        
        # Cart items
        for item in self.cart:
            item_frame = ctk.CTkFrame(cart_frame)
            item_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(item_frame, text=item['name'], width=200).pack(side="left", padx=10)
            ctk.CTkLabel(item_frame, text=f"${item['price']:.2f}", width=100).pack(side="left", padx=10)
            ctk.CTkLabel(item_frame, text=str(item['quantity']), width=100).pack(side="left", padx=10)
            ctk.CTkLabel(item_frame, text=f"${item['price'] * item['quantity']:.2f}", width=100).pack(side="left", padx=10)
            
            remove_button = ctk.CTkButton(
                item_frame,
                text="Remove",
                width=100,
                fg_color="red",
                hover_color="darkred",
                command=lambda i=item: self.remove_from_cart(i)
            )
            remove_button.pack(side="left", padx=10)
        
        # Total and actions
        bottom_frame = ctk.CTkFrame(self.content_frame)
        bottom_frame.pack(fill="x", padx=20, pady=20)
        
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        total_label = ctk.CTkLabel(
            bottom_frame,
            text=f"Total: ${total:.2f}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        total_label.pack(side="right", padx=20)
        
        checkout_button = ctk.CTkButton(
            bottom_frame,
            text="Place Order",
            width=150,
            height=40,
            font=ctk.CTkFont(size=16),
            command=self.place_order
        )
        checkout_button.pack(side="right", padx=10)
        
        continue_button = ctk.CTkButton(
            bottom_frame,
            text="Continue Shopping",
            width=150,
            height=40,
            font=ctk.CTkFont(size=16),
            command=self.show_products
        )
        continue_button.pack(side="left", padx=10)
    
    def remove_from_cart(self, item):
        self.cart.remove(item)
        self.update_cart_button()
        self.show_cart()
    
    def place_order(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Your cart is empty. Add products to cart first.")
            return
        
        # Place order directly without asking for shipping address
        address = "Not provided"  # Default address
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                
                # Calculate total
                total = sum(item['price'] * item['quantity'] for item in self.cart)
                
                # Create order
                cursor.execute(
                    """INSERT INTO orders (customer_id, total_amount, shipping_address, status)
                    VALUES (%s, %s, %s, 'pending')""",
                    (self.main_app.current_user['id'], total, address)
                )
                order_id = cursor.lastrowid
                
                # Add order items and update inventory
                for item in self.cart:
                    cursor.execute(
                        """INSERT INTO order_items (order_id, product_id, quantity, price)
                        VALUES (%s, %s, %s, %s)""",
                        (order_id, item['product_id'], item['quantity'], item['price'])
                    )
                    
                    # Update product quantity
                    cursor.execute(
                        """UPDATE products SET quantity = quantity - %s WHERE id = %s""",
                        (item['quantity'], item['product_id'])
                    )
                
                connection.commit()
                cursor.close()
                connection.close()
                
                # Clear cart
                self.cart = []
                self.update_cart_button()
                
                messagebox.showinfo("Success", f"Order #{order_id} placed successfully!")
                self.show_orders()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to place order: {e}")
    
    def show_orders(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="My Orders",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Get customer orders
                cursor.execute(
                    """SELECT * FROM orders 
                    WHERE customer_id = %s 
                    ORDER BY order_date DESC""",
                    (self.main_app.current_user['id'],)
                )
                orders = cursor.fetchall()
                
                if not orders:
                    no_orders_label = ctk.CTkLabel(
                        self.content_frame,
                        text="You have no orders yet",
                        font=ctk.CTkFont(size=16)
                    )
                    no_orders_label.pack(pady=50)
                else:
                    # Orders frame with scrollbar
                    orders_container = ctk.CTkFrame(self.content_frame)
                    orders_container.pack(fill="both", expand=True, padx=20, pady=10)
                    
                    for order in orders:
                        order_frame = ctk.CTkFrame(orders_container)
                        order_frame.pack(fill="x", padx=10, pady=10)
                        
                        # Order header
                        header_frame = ctk.CTkFrame(order_frame)
                        header_frame.pack(fill="x", padx=10, pady=10)
                        
                        ctk.CTkLabel(
                            header_frame,
                            text=f"Order #{order['id']}",
                            font=ctk.CTkFont(size=16, weight="bold")
                        ).pack(side="left", padx=10)
                        
                        ctk.CTkLabel(
                            header_frame,
                            text=f"Date: {order['order_date'].strftime('%Y-%m-%d %H:%M')}",
                            font=ctk.CTkFont(size=12)
                        ).pack(side="left", padx=10)
                        
                        # Status badge
                        status_colors = {
                            'pending': 'orange',
                            'processing': 'blue',
                            'shipped': 'purple',
                            'delivered': 'green',
                            'cancelled': 'red'
                        }
                        ctk.CTkLabel(
                            header_frame,
                            text=order['status'].upper(),
                            font=ctk.CTkFont(size=12, weight="bold"),
                            text_color=status_colors.get(order['status'], 'gray')
                        ).pack(side="right", padx=10)
                        
                        ctk.CTkLabel(
                            header_frame,
                            text=f"Total: ${order['total_amount']:.2f}",
                            font=ctk.CTkFont(size=14, weight="bold")
                        ).pack(side="right", padx=10)
                        
                        # Get order items
                        cursor.execute(
                            """SELECT oi.*, p.name as product_name
                            FROM order_items oi
                            JOIN products p ON oi.product_id = p.id
                            WHERE oi.order_id = %s""",
                            (order['id'],)
                        )
                        items = cursor.fetchall()
                        
                        # Items frame
                        items_frame = ctk.CTkFrame(order_frame)
                        items_frame.pack(fill="x", padx=10, pady=(0, 10))
                        
                        for item in items:
                            item_text = f"  • {item['product_name']} x {item['quantity']} - ${item['price'] * item['quantity']:.2f}"
                            ctk.CTkLabel(
                                items_frame,
                                text=item_text,
                                font=ctk.CTkFont(size=12)
                            ).pack(anchor="w", padx=10, pady=2)
                        
                        # Shipping address
                        if order['shipping_address']:
                            ctk.CTkLabel(
                                order_frame,
                                text=f"Shipping to: {order['shipping_address']}",
                                font=ctk.CTkFont(size=11),
                                text_color="gray"
                            ).pack(anchor="w", padx=20, pady=(0, 10))
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load orders: {e}")
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.main_app.logout()
