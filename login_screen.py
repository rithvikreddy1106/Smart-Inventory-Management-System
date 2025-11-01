"""
Standalone Login Screen
Run this file independently to test the login UI
Usage: python login_screen.py
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

# LoginScreen class for use in main app (as modal window)
class LoginScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.title("Login - SIMS")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Add hero image
        try:
            hero_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "cat2.jpg")
            hero_image = Image.open(hero_path)
            hero_image = hero_image.resize((300, 200), Image.LANCZOS)
            hero_photo = ImageTk.PhotoImage(hero_image)
            
            hero_label = ctk.CTkLabel(main_frame, image=hero_photo, text="")
            hero_label.image = hero_photo
            hero_label.pack(pady=(20, 10))
        except Exception as e:
            print(f"Could not load hero image: {e}")
        
        # Create title
        title_label = ctk.CTkLabel(main_frame, text="Login to SIMS", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(10, 30))
        
        # Create form
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=30)
        
        # Email field
        email_label = ctk.CTkLabel(form_frame, text="Email:", font=ctk.CTkFont(size=14))
        email_label.pack(anchor="w", pady=(0, 5))
        self.email_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="Enter your email")
        self.email_entry.pack(pady=(0, 20))
        
        # Password field
        password_label = ctk.CTkLabel(form_frame, text="Password:", font=ctk.CTkFont(size=14))
        password_label.pack(anchor="w", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(form_frame, width=350, height=40, placeholder_text="Enter your password", show="*")
        self.password_entry.pack(pady=(0, 25))
        
        # Login button
        login_button = ctk.CTkButton(form_frame, text="Login", font=ctk.CTkFont(size=16), width=350, height=45, command=self.login)
        login_button.pack(pady=(10, 0))
        
        # Register info
        register_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        register_frame.pack(fill="x", pady=15)
        
        register_label = ctk.CTkLabel(register_frame, text="Don't have an account? Register", font=ctk.CTkFont(size=12))
        register_label.pack()
        
        # Set focus to email entry
        self.email_entry.focus_set()
        
        # Bind Enter key to login
        self.bind("<Return>", lambda event: self.login())
    
    def hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        try:
            connection = db_config.create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Get user by email
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()
                
                if user and user['password'] == self.hash_password(password):
                    # Check if staff is approved
                    if user['user_type'] == 'staff' and not user['is_approved']:
                        messagebox.showwarning("Account Pending", "Your staff account is pending approval by an administrator.")
                        return
                    
                    # Successful login
                    messagebox.showinfo("Success", f"Welcome, {user['full_name']}!")
                    self.destroy()  # Close login window
                    
                    # Pass user data to main application
                    self.master.login_success(user)
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password")
                
                cursor.close()
                connection.close()
                
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def open_register(self):
        self.destroy()
        from user_registration import RegisterScreen
        register_window = RegisterScreen(self.master)
        register_window.grab_set()


# Standalone mode for testing
if __name__ == "__main__":
    db_config.create_database()
    
    class StandaloneApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("SIMS - Standalone Login")
            self.geometry("1x1")
            self.withdraw()
            
            # Open login screen
            login = LoginScreen(self)
            login.grab_set()
            
        def login_success(self, user_data):
            messagebox.showinfo("Login Successful", 
                f"Welcome, {user_data['full_name']}!\n\n"
                f"User Type: {user_data['user_type'].capitalize()}\n\n"
                f"Note: This is standalone mode.\n"
                f"Run main.py for the full application.")
            self.destroy()
    
    app = StandaloneApp()
    app.mainloop()
