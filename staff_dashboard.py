import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from mysql.connector import Error
import db_config

class StaffDashboard:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        
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
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.container, height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            header_frame,
            text=f"Staff Dashboard - Welcome, {self.main_app.current_user['full_name']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        welcome_label.pack(side="left", padx=20)
        
        # Logout button
        logout_button = ctk.CTkButton(
            header_frame,
            text="Logout",
            font=ctk.CTkFont(size=14),
            width=100,
            command=self.logout
        )
        logout_button.pack(side="right", padx=20)
    
    def create_navigation(self):
        nav_frame = ctk.CTkFrame(self.container, height=50)
        nav_frame.pack(fill="x", padx=10, pady=5)
        nav_frame.pack_propagate(False)
        
        # Navigation buttons
        dashboard_btn = ctk.CTkButton(
            nav_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=14),
            width=120,
            command=self.show_dashboard
        )
        dashboard_btn.pack(side="left", padx=10)
        
        orders_btn = ctk.CTkButton(
            nav_frame,
            text="Manage Orders",
            font=ctk.CTkFont(size=14),
            width=120,
            command=self.show_orders
        )
        orders_btn.pack(side="left", padx=10)
        
        inventory_btn = ctk.CTkButton(
            nav_frame,
            text="Manage Inventory",
            font=ctk.CTkFont(size=14),
            width=140,
            command=self.show_inventory
        )
        inventory_btn.pack(side="left", padx=10)
        
        alerts_btn = ctk.CTkButton(
            nav_frame,
            text="Low Stock Alerts",
            font=ctk.CTkFont(size=14),
            width=140,
            command=self.show_alerts
        )
        alerts_btn.pack(side="left", padx=10)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Staff Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Stats frame
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                
                # Get pending orders count
                cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'")
                pending_orders = cursor.fetchone()[0]
                
                # Get low stock products count
                cursor.execute("SELECT COUNT(*) FROM products WHERE quantity <= reorder_level")
                low_stock = cursor.fetchone()[0]
                
                # Get total products
                cursor.execute("SELECT COUNT(*) FROM products")
                total_products = cursor.fetchone()[0]
                
                # Get processing orders
                cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'processing'")
                processing_orders = cursor.fetchone()[0]
                
                cursor.close()
                connection.close()
                
                # Display stats
                self.create_stat_card(stats_frame, "Pending Orders", pending_orders, "orange").pack(side="left", padx=20, pady=20, expand=True)
                self.create_stat_card(stats_frame, "Processing Orders", processing_orders, "blue").pack(side="left", padx=20, pady=20, expand=True)
                self.create_stat_card(stats_frame, "Low Stock Items", low_stock, "red").pack(side="left", padx=20, pady=20, expand=True)
                self.create_stat_card(stats_frame, "Total Products", total_products, "green").pack(side="left", padx=20, pady=20, expand=True)
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load dashboard: {e}")
        
        # Quick actions
        actions_frame = ctk.CTkFrame(self.content_frame)
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Process Pending Orders",
            width=200,
            height=40,
            command=self.show_orders
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Add New Product",
            width=200,
            height=40,
            command=self.add_product
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Check Low Stock",
            width=200,
            height=40,
            command=self.show_alerts
        ).pack(side="left", padx=10)
    
    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, width=200, height=120)
        card.pack_propagate(False)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=color
        ).pack(pady=(0, 20))
        
        return card
    
    def show_orders(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Manage Orders",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Filter frame
        filter_frame = ctk.CTkFrame(self.content_frame)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Filter by Status:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        
        self.order_status_var = tk.StringVar(value="All")
        status_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.order_status_var,
            values=["All", "pending", "approved", "rejected"],
            width=150,
            command=lambda x: self.load_orders()
        )
        status_menu.pack(side="left", padx=10)
        
        # Orders frame with scrollbar
        orders_container = ctk.CTkFrame(self.content_frame)
        orders_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(orders_container, bg=self.content_frame.cget("fg_color")[1])
        scrollbar = ctk.CTkScrollbar(orders_container, command=canvas.yview)
        self.orders_frame = ctk.CTkFrame(canvas)
        
        self.orders_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.orders_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.load_orders()
    
    def load_orders(self):
        # Clear orders frame
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Build query
                query = """
                    SELECT o.*, u.full_name as customer_name, u.email as customer_email
                    FROM orders o
                    JOIN users u ON o.customer_id = u.id
                """
                
                status_filter = self.order_status_var.get()
                if status_filter != "All":
                    query += " WHERE o.status = %s"
                    cursor.execute(query + " ORDER BY o.order_date DESC", (status_filter,))
                else:
                    cursor.execute(query + " ORDER BY o.order_date DESC")
                
                orders = cursor.fetchall()
                
                if not orders:
                    no_orders_label = ctk.CTkLabel(
                        self.orders_frame,
                        text="No orders found",
                        font=ctk.CTkFont(size=16)
                    )
                    no_orders_label.pack(pady=50)
                else:
                    for order in orders:
                        self.create_order_card(order, cursor)
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load orders: {e}")
    
    def create_order_card(self, order, cursor):
        card = ctk.CTkFrame(self.orders_frame)
        card.pack(fill="x", padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(card)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"Order #{order['id']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"Customer: {order['customer_name']}",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            header_frame,
            text=f"Date: {order['order_date'].strftime('%Y-%m-%d %H:%M')}",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=10)
        
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
        
        # Items
        items_frame = ctk.CTkFrame(card)
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
                card,
                text=f"Shipping to: {order['shipping_address']}",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=(0, 10))
        
        # Actions
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        # Current status
        status_colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        
        ctk.CTkLabel(
            actions_frame,
            text=f"Status: {order['status'].upper()}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=status_colors.get(order['status'], 'gray')
        ).pack(side="left", padx=10)
        
        # Status change buttons
        if order['status'] == 'pending':
            ctk.CTkButton(
                actions_frame,
                text="✓ Approve Order",
                width=130,
                fg_color="green",
                hover_color="darkgreen",
                command=lambda: self.update_order_status(order['id'], 'approved')
            ).pack(side="right", padx=5)
            
            ctk.CTkButton(
                actions_frame,
                text="✗ Reject Order",
                width=120,
                fg_color="red",
                hover_color="darkred",
                command=lambda: self.update_order_status(order['id'], 'rejected')
            ).pack(side="right", padx=5)
    
    def update_order_status(self, order_id, new_status):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE orders SET status = %s WHERE id = %s",
                    (new_status, order_id)
                )
                connection.commit()
                cursor.close()
                connection.close()
                
                messagebox.showinfo("Success", f"Order #{order_id} status updated to {new_status}")
                self.load_orders()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to update order status: {e}")
    
    def show_inventory(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Manage Inventory",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.content_frame)
        action_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            action_frame,
            text="Add New Product",
            width=150,
            command=self.add_product
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="Refresh",
            width=100,
            command=self.load_products
        ).pack(side="left", padx=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        
        self.product_search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Search products...")
        self.product_search_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(search_frame, text="Search", width=100, command=self.load_products).pack(side="left", padx=10)
        
        # Products table
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ID", "Name", "Category", "Price", "Quantity", "Reorder Level")
        
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            if col == "Name":
                self.products_tree.column(col, width=200)
            elif col == "Category":
                self.products_tree.column(col, width=150)
            else:
                self.products_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons for selected product
        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Edit Selected",
            width=150,
            command=self.edit_product
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            width=150,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_product
        ).pack(side="left", padx=10)
        
        self.load_products()
    
    def load_products(self):
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Build query
                query = """
                    SELECT p.*, c.name as category_name
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.id
                """
                
                search_term = self.product_search_entry.get().strip()
                if search_term:
                    query += " WHERE p.name LIKE %s OR p.description LIKE %s"
                    cursor.execute(query + " ORDER BY p.name", (f"%{search_term}%", f"%{search_term}%"))
                else:
                    cursor.execute(query + " ORDER BY p.name")
                
                products = cursor.fetchall()
                
                for product in products:
                    # Highlight low stock items
                    tag = "low_stock" if product['quantity'] <= product['reorder_level'] else ""
                    
                    self.products_tree.insert("", "end", values=(
                        product['id'],
                        product['name'],
                        product['category_name'] or 'N/A',
                        f"${product['price']:.2f}",
                        product['quantity'],
                        product['reorder_level']
                    ), tags=(tag,))
                
                # Configure tag colors
                self.products_tree.tag_configure("low_stock", background="#ffcccc")
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")
    
    def add_product(self):
        AddProductDialog(self, self.main_app)
    
    def edit_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
        
        product_id = self.products_tree.item(selected[0])['values'][0]
        EditProductDialog(self, self.main_app, product_id)
    
    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        product_name = self.products_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            product_id = self.products_tree.item(selected[0])['values'][0]
            
            try:
                connection = db_config.create_connection()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Product deleted successfully")
                    self.load_products()
                    
            except Error as e:
                messagebox.showerror("Error", f"Failed to delete product: {e}")
    
    def show_alerts(self):
        self.clear_content()
        
        # Title
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Low Stock Alerts",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                cursor.execute("""
                    SELECT p.*, c.name as category_name, s.name as supplier_name
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.id
                    LEFT JOIN suppliers s ON p.supplier_id = s.id
                    WHERE p.quantity <= p.reorder_level
                    ORDER BY p.quantity ASC
                """)
                
                low_stock_products = cursor.fetchall()
                
                if not low_stock_products:
                    ctk.CTkLabel(
                        self.content_frame,
                        text="✓ All products are well-stocked!",
                        font=ctk.CTkFont(size=18),
                        text_color="green"
                    ).pack(pady=50)
                else:
                    # Alerts frame
                    alerts_frame = ctk.CTkFrame(self.content_frame)
                    alerts_frame.pack(fill="both", expand=True, padx=20, pady=10)
                    
                    for product in low_stock_products:
                        alert_card = ctk.CTkFrame(alerts_frame)
                        alert_card.pack(fill="x", padx=10, pady=10)
                        
                        # Product info
                        info_frame = ctk.CTkFrame(alert_card, fg_color="transparent")
                        info_frame.pack(fill="x", padx=10, pady=10)
                        
                        ctk.CTkLabel(
                            info_frame,
                            text=f"⚠️ {product['name']}",
                            font=ctk.CTkFont(size=16, weight="bold"),
                            text_color="red"
                        ).pack(side="left", padx=10)
                        
                        ctk.CTkLabel(
                            info_frame,
                            text=f"Current Stock: {product['quantity']}",
                            font=ctk.CTkFont(size=14),
                            text_color="orange"
                        ).pack(side="left", padx=10)
                        
                        ctk.CTkLabel(
                            info_frame,
                            text=f"Reorder Level: {product['reorder_level']}",
                            font=ctk.CTkFont(size=14)
                        ).pack(side="left", padx=10)
                        
                        if product['supplier_name']:
                            ctk.CTkLabel(
                                info_frame,
                                text=f"Supplier: {product['supplier_name']}",
                                font=ctk.CTkFont(size=12),
                                text_color="gray"
                            ).pack(side="right", padx=10)
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load alerts: {e}")
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.main_app.logout()


class AddProductDialog(ctk.CTkToplevel):
    def __init__(self, parent, main_app):
        super().__init__(parent.main_app)
        self.parent = parent
        self.main_app = main_app
        
        self.title("Add New Product")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create form
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            form_frame,
            text="Add New Product",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 20))
        
        # Product Name
        ctk.CTkLabel(form_frame, text="Product Name:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.name_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter product name")
        self.name_entry.pack(padx=20, pady=(0, 10))
        
        # Description
        ctk.CTkLabel(form_frame, text="Description:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.desc_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter product description")
        self.desc_entry.pack(padx=20, pady=(0, 10))
        
        # Category
        ctk.CTkLabel(form_frame, text="Category:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.category_var = tk.StringVar()
        self.category_menu = ctk.CTkOptionMenu(form_frame, variable=self.category_var, values=self.get_categories(), width=400)
        self.category_menu.pack(padx=20, pady=(0, 10))
        
        # Supplier
        ctk.CTkLabel(form_frame, text="Supplier:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.supplier_var = tk.StringVar()
        self.supplier_menu = ctk.CTkOptionMenu(form_frame, variable=self.supplier_var, values=self.get_suppliers(), width=400)
        self.supplier_menu.pack(padx=20, pady=(0, 10))
        
        # Price
        ctk.CTkLabel(form_frame, text="Price:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.price_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter price (e.g., 19.99)")
        self.price_entry.pack(padx=20, pady=(0, 10))
        
        # Quantity
        ctk.CTkLabel(form_frame, text="Quantity:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.quantity_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter initial quantity")
        self.quantity_entry.pack(padx=20, pady=(0, 10))
        
        # Reorder Level
        ctk.CTkLabel(form_frame, text="Reorder Level:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.reorder_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter reorder level (default: 10)")
        self.reorder_entry.insert(0, "10")
        self.reorder_entry.pack(padx=20, pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Add Product",
            width=150,
            command=self.add_product
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            fg_color="gray",
            command=self.destroy
        ).pack(side="left", padx=10)
    
    def get_categories(self):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM categories ORDER BY name")
                categories = [row[0] for row in cursor.fetchall()]
                cursor.close()
                connection.close()
                return categories if categories else ["No categories"]
        except Error as e:
            print(f"Error: {e}")
        return ["No categories"]
    
    def get_suppliers(self):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM suppliers ORDER BY name")
                suppliers = [row[0] for row in cursor.fetchall()]
                cursor.close()
                connection.close()
                return suppliers if suppliers else ["No suppliers"]
        except Error as e:
            print(f"Error: {e}")
        return ["No suppliers"]
    
    def add_product(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        category = self.category_var.get()
        supplier = self.supplier_var.get()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        reorder_level = self.reorder_entry.get().strip()
        
        if not name or not price or not quantity:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
            reorder_level = int(reorder_level)
            
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                
                # Get category ID
                cursor.execute("SELECT id FROM categories WHERE name = %s", (category,))
                category_result = cursor.fetchone()
                category_id = category_result[0] if category_result else None
                
                # Get supplier ID
                cursor.execute("SELECT id FROM suppliers WHERE name = %s", (supplier,))
                supplier_result = cursor.fetchone()
                supplier_id = supplier_result[0] if supplier_result else None
                
                # Insert product
                cursor.execute(
                    """INSERT INTO products (name, description, category_id, supplier_id, price, quantity, reorder_level)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (name, description, category_id, supplier_id, price, quantity, reorder_level)
                )
                
                connection.commit()
                cursor.close()
                connection.close()
                
                messagebox.showinfo("Success", "Product added successfully!")
                self.destroy()
                self.parent.load_products()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price, quantity, and reorder level")
        except Error as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")


class EditProductDialog(ctk.CTkToplevel):
    def __init__(self, parent, main_app, product_id):
        super().__init__(parent.main_app)
        self.parent = parent
        self.main_app = main_app
        self.product_id = product_id
        
        self.title("Edit Product")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create form
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            form_frame,
            text="Edit Product",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 20))
        
        # Product Name
        ctk.CTkLabel(form_frame, text="Product Name:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.name_entry = ctk.CTkEntry(form_frame, width=400)
        self.name_entry.pack(padx=20, pady=(0, 10))
        
        # Description
        ctk.CTkLabel(form_frame, text="Description:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.desc_entry = ctk.CTkEntry(form_frame, width=400)
        self.desc_entry.pack(padx=20, pady=(0, 10))
        
        # Category
        ctk.CTkLabel(form_frame, text="Category:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.category_var = tk.StringVar()
        self.category_menu = ctk.CTkOptionMenu(form_frame, variable=self.category_var, values=self.get_categories(), width=400)
        self.category_menu.pack(padx=20, pady=(0, 10))
        
        # Supplier
        ctk.CTkLabel(form_frame, text="Supplier:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.supplier_var = tk.StringVar()
        self.supplier_menu = ctk.CTkOptionMenu(form_frame, variable=self.supplier_var, values=self.get_suppliers(), width=400)
        self.supplier_menu.pack(padx=20, pady=(0, 10))
        
        # Price
        ctk.CTkLabel(form_frame, text="Price:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.price_entry = ctk.CTkEntry(form_frame, width=400)
        self.price_entry.pack(padx=20, pady=(0, 10))
        
        # Quantity
        ctk.CTkLabel(form_frame, text="Quantity:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.quantity_entry = ctk.CTkEntry(form_frame, width=400)
        self.quantity_entry.pack(padx=20, pady=(0, 10))
        
        # Reorder Level
        ctk.CTkLabel(form_frame, text="Reorder Level:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.reorder_entry = ctk.CTkEntry(form_frame, width=400)
        self.reorder_entry.pack(padx=20, pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Update Product",
            width=150,
            command=self.update_product
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            fg_color="gray",
            command=self.destroy
        ).pack(side="left", padx=10)
        
        # Load product data
        self.load_product_data()
    
    def get_categories(self):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM categories ORDER BY name")
                categories = [row[0] for row in cursor.fetchall()]
                cursor.close()
                connection.close()
                return categories if categories else ["No categories"]
        except Error as e:
            print(f"Error: {e}")
        return ["No categories"]
    
    def get_suppliers(self):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM suppliers ORDER BY name")
                suppliers = [row[0] for row in cursor.fetchall()]
                cursor.close()
                connection.close()
                return suppliers if suppliers else ["No suppliers"]
        except Error as e:
            print(f"Error: {e}")
        return ["No suppliers"]
    
    def load_product_data(self):
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT p.*, c.name as category_name, s.name as supplier_name
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.id
                    LEFT JOIN suppliers s ON p.supplier_id = s.id
                    WHERE p.id = %s
                """, (self.product_id,))
                
                product = cursor.fetchone()
                
                if product:
                    self.name_entry.insert(0, product['name'])
                    self.desc_entry.insert(0, product['description'] or '')
                    self.category_var.set(product['category_name'] or 'No categories')
                    self.supplier_var.set(product['supplier_name'] or 'No suppliers')
                    self.price_entry.insert(0, str(product['price']))
                    self.quantity_entry.insert(0, str(product['quantity']))
                    self.reorder_entry.insert(0, str(product['reorder_level']))
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load product data: {e}")
    
    def update_product(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        category = self.category_var.get()
        supplier = self.supplier_var.get()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        reorder_level = self.reorder_entry.get().strip()
        
        if not name or not price or not quantity:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
            reorder_level = int(reorder_level)
            
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor()
                
                # Get category ID
                cursor.execute("SELECT id FROM categories WHERE name = %s", (category,))
                category_result = cursor.fetchone()
                category_id = category_result[0] if category_result else None
                
                # Get supplier ID
                cursor.execute("SELECT id FROM suppliers WHERE name = %s", (supplier,))
                supplier_result = cursor.fetchone()
                supplier_id = supplier_result[0] if supplier_result else None
                
                # Update product
                cursor.execute(
                    """UPDATE products 
                    SET name = %s, description = %s, category_id = %s, supplier_id = %s, 
                        price = %s, quantity = %s, reorder_level = %s
                    WHERE id = %s""",
                    (name, description, category_id, supplier_id, price, quantity, reorder_level, self.product_id)
                )
                
                connection.commit()
                cursor.close()
                connection.close()
                
                messagebox.showinfo("Success", "Product updated successfully!")
                self.destroy()
                self.parent.load_products()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price, quantity, and reorder level")
        except Error as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")
