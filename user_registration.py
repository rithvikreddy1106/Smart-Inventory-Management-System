"""
User Registration Screen Component
"""
import os
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
import db_config

# Set appearance mode and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

# Set custom orange theme
ctk.ThemeManager.theme["CTkButton"]["fg_color"] = ["#FF8C00", "#FF6500"]
ctk.ThemeManager.theme["CTkButton"]["hover_color"] = ["#FF6500", "#FF4500"]

class RegisterScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.title("Register - SIMS")
        self.geometry("900x700")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with two columns
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Hero image
        left_frame = ctk.CTkFrame(main_frame, width=320)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        try:
            hero_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "cat2.jpg")
            hero_image = Image.open(hero_path)
            hero_image = hero_image.resize((300, 400), Image.LANCZOS)
            hero_photo = ImageTk.PhotoImage(hero_image)
            
            hero_label = ctk.CTkLabel(left_frame, image=hero_photo, text="")
            hero_label.image = hero_photo
            hero_label.pack(expand=True)
        except Exception as e:
            print(f"Could not load hero image: {e}")
        
        # Right side - Form
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Create title
        title_label = ctk.CTkLabel(right_frame, text="Register for SIMS", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 20))
        
        # Create form
        form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # Full Name field
        name_label = ctk.CTkLabel(form_frame, text="Full Name:", font=ctk.CTkFont(size=14))
        name_label.pack(anchor="w", pady=(0, 5))
        self.name_entry = ctk.CTkEntry(form_frame, height=35, placeholder_text="Enter your full name")
        self.name_entry.pack(fill="x", pady=(0, 10))
        
        # Email field
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=14))
        email_label.pack(anchor="w", pady=(0, 5))
        self.email_entry = ctk.CTkEntry(form_frame, height=35, placeholder_text="Enter your email")
        self.email_entry.pack(fill="x", pady=(0, 10))
        
        # Phone Number field
        phone_label = ctk.CTkLabel(form_frame, text="Phone Number:", font=ctk.CTkFont(size=14))
        phone_label.pack(anchor="w", pady=(0, 5))
        self.phone_entry = ctk.CTkEntry(form_frame, height=35, placeholder_text="Enter your phone number")
        self.phone_entry.pack(fill="x", pady=(0, 10))
        
        # Password field
        password_label = ctk.CTkLabel(form_frame, text="Password:", font=ctk.CTkFont(size=14))
        password_label.pack(anchor="w", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(form_frame, height=35, placeholder_text="Min 6 characters", show="*")
        self.password_entry.pack(fill="x", pady=(0, 10))
        
        # Confirm Password field
        confirm_password_label = ctk.CTkLabel(form_frame, text="Confirm Password:", font=ctk.CTkFont(size=14))
        confirm_password_label.pack(anchor="w", pady=(0, 5))
        self.confirm_password_entry = ctk.CTkEntry(form_frame, height=35, placeholder_text="Confirm your password", show="*")
        self.confirm_password_entry.pack(fill="x", pady=(0, 10))
        
        # User Type selection
        user_type_label = ctk.CTkLabel(form_frame, text="Register as:", font=ctk.CTkFont(size=14))
        user_type_label.pack(anchor="w", pady=(0, 10))
        
        # Radio buttons frame
        radio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        radio_frame.pack(fill="x", pady=(0, 20))
        
        self.user_type_var = tk.StringVar(value="customer")
        
        customer_radio = ctk.CTkRadioButton(radio_frame, text="Customer (Can place orders)", variable=self.user_type_var, value="customer", font=ctk.CTkFont(size=13))
        customer_radio.pack(side="left", padx=(0, 30))
        
        staff_radio = ctk.CTkRadioButton(radio_frame, text="Staff (Requires admin approval)", variable=self.user_type_var, value="staff", font=ctk.CTkFont(size=13))
        staff_radio.pack(side="left")
        
        # Register button
        register_button = ctk.CTkButton(form_frame, text="Register", font=ctk.CTkFont(size=16), height=40, command=self.register)
        register_button.pack(fill="x", pady=(15, 10))
        
        # Login link
        login_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_frame.pack(fill="x", pady=5)
        
        login_label = ctk.CTkLabel(login_frame, text="Already have an account?", font=ctk.CTkFont(size=12))
        login_label.pack(side="left")
        
        login_link = ctk.CTkButton(login_frame, text="Login", font=ctk.CTkFont(size=12), fg_color="transparent", hover=False, command=self.open_login)
        login_link.pack(side="left", padx=5)
        
        # Set focus to name entry
        self.name_entry.focus_set()
    
    def hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self):
        full_name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        user_type = self.user_type_var.get()
        
        # Validate inputs
        if not full_name or not email or not phone or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Check if email already exists
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s",
                    (email,)
                )
                existing_user = cursor.fetchone()
                
                if existing_user:
                    messagebox.showerror("Error", "Email already registered")
                    return
                
                # Set approval status based on user type
                is_approved = True if user_type == "customer" else False
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO users (full_name, email, phone_number, password, user_type, is_approved) VALUES (%s, %s, %s, %s, %s, %s)",
                    (full_name, email, phone, self.hash_password(password), user_type, is_approved)
                )
                connection.commit()
                
                cursor.close()
                connection.close()
                
                # Show success message
                if user_type == "staff":
                    messagebox.showinfo("Registration Successful", 
                        "Your staff account has been created and is pending approval by an administrator.")
                else:
                    messagebox.showinfo("Registration Successful", 
                        "Your account has been created successfully. You can now login.")
                
                # Close register window and open login
                self.destroy()
                from login_screen import LoginScreen
                login_window = LoginScreen(self.master)
                login_window.grab_set()
                
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def open_login(self):
        self.destroy()
        from login_screen import LoginScreen
        login_window = LoginScreen(self.master)
        login_window.grab_set()


# Standalone mode for testing
if __name__ == "__main__":
    db_config.create_database()
    
    class StandaloneApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("SIMS - Standalone Registration")
            self.geometry("1x1")
            self.withdraw()
            
            # Open registration screen
            register = RegisterScreen(self)
            register.grab_set()
        
        def login_success(self, user_data):
            # Not used in registration, but needed for compatibility
            pass
    
    app = StandaloneApp()
    app.mainloop()
