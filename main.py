import os
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import db_config
from login_screen import LoginScreen
from user_registration import RegisterScreen
from customer_dashboard import CustomerDashboard
from staff_dashboard import StaffDashboard
from admin_dashboard import AdminDashboard

# Initialize database
db_config.create_database()

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

# Set custom orange theme
ctk.ThemeManager.theme["CTkButton"]["fg_color"] = ["#FF8C00", "#FF6500"]  # Orange
ctk.ThemeManager.theme["CTkButton"]["hover_color"] = ["#FF6500", "#FF4500"]  # Darker orange

class InventoryManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Smart Inventory Management System")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        
        # Load and set icon
        try:
            self.iconpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "logo1.png")
            self.iconphoto(False, ImageTk.PhotoImage(Image.open(self.iconpath)))
        except:
            pass
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create home screen
        self.create_home_screen()
        
        # Current user data
        self.current_user = None
    
    def create_home_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create header frame
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 40))
        
        # Load logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "logo1.png")
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((100, 100), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Create logo label
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.image = logo_photo
            logo_label.pack(side="left", padx=(0, 20))
        except:
            pass
        
        # Create title label
        title_label = ctk.CTkLabel(header_frame, text="Smart Inventory Management System", font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(side="left", padx=20)
        
        # Create content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add hero image
        try:
            hero_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "cat2.jpg")
            hero_image = Image.open(hero_path)
            hero_image = hero_image.resize((400, 300), Image.LANCZOS)
            hero_photo = ImageTk.PhotoImage(hero_image)
            
            hero_label = ctk.CTkLabel(content_frame, image=hero_photo, text="")
            hero_label.image = hero_photo
            hero_label.pack(pady=(40, 20))
        except Exception as e:
            print(f"Could not load hero image: {e}")
        
        # Create welcome message
        welcome_label = ctk.CTkLabel(content_frame, text="Welcome to SIMS", font=ctk.CTkFont(size=28, weight="bold"))
        welcome_label.pack(pady=(20, 10))
        
        description_label = ctk.CTkLabel(content_frame, text="Manage your inventory, track orders, and monitor sales with ease.", font=ctk.CTkFont(size=16))
        description_label.pack(pady=(0, 30))
        
        # Create buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        # Create login button
        login_button = ctk.CTkButton(buttons_frame, text="Login", font=ctk.CTkFont(size=18), width=220, height=55, command=self.open_login)
        login_button.pack(side="left", padx=20)
        
        # Create register button
        register_button = ctk.CTkButton(buttons_frame, text="Register", font=ctk.CTkFont(size=18), width=220, height=55, command=self.open_register)
        register_button.pack(side="left", padx=20)
        
        # Create footer
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=40)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        
        footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Smart Inventory Management System", font=ctk.CTkFont(size=12))
        footer_label.pack(side="right")
    
    def open_login(self):
        login_window = LoginScreen(self)
        login_window.grab_set()  # Make the window modal
    
    def open_register(self):
        register_window = RegisterScreen(self)
        register_window.grab_set()  # Make the window modal
    
    def login_success(self, user_data):
        self.current_user = user_data
        
        # Open appropriate dashboard based on user type
        if user_data["user_type"] == "customer":
            self.open_customer_dashboard()
        elif user_data["user_type"] == "staff":
            self.open_staff_dashboard()
        elif user_data["user_type"] == "admin":
            self.open_admin_dashboard()
    
    def open_customer_dashboard(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create customer dashboard
        CustomerDashboard(self.main_frame, self)
    
    def open_staff_dashboard(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create staff dashboard
        StaffDashboard(self.main_frame, self)
    
    def open_admin_dashboard(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create admin dashboard
        AdminDashboard(self.main_frame, self)
    
    def logout(self):
        self.current_user = None
        self.create_home_screen()

if __name__ == "__main__":
    app = InventoryManagementSystem()
    app.mainloop()
