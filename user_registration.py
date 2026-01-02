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
        
        self.title("Smart Inventory Management System - Register")
        # Make full screen and resizable
        self.state('zoomed')  # Windows full screen
        self.resizable(True, True)
        
        # -------------------- Main Container Frame (50/50 split) --------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure grid for two equal columns: 0 (image), 1 (form)
        self.main_frame.grid_columnconfigure(0, weight=1) 
        self.main_frame.grid_columnconfigure(1, weight=2) 
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # -------------------- 1. Left Frame (Image - 50% of screen) --------------------
        self.image_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFE5B4")  # Light orange background
        self.image_frame.grid(row=0, column=0, sticky="nsew")
        
        # --- Load and Display menu_im.png Image ---
        try:
            bg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "menu_im.png")
            if not os.path.exists(bg_path):
                bg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "category.jpg")
            if not os.path.exists(bg_path):
                bg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "background.png")
            
            # Load image and create CTkImage for better scaling
            img = Image.open(bg_path)
            # Use CTkImage for better HighDPI support - will resize dynamically
            self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
            
            # Use CTkLabel to display the image
            image_label = ctk.CTkLabel(self.image_frame, image=self.bg_image, text="", fg_color="transparent")
            image_label.pack(fill="both", expand=True)  # Fill the frame
            
            # Update image size after window is displayed
            self.after(100, lambda: self._resize_image(image_label, img))
            
        except Exception as e:
            print(f"Could not load side image: {e}")
            ctk.CTkLabel(
                self.image_frame, 
                text="Smart Inventory", 
                text_color="#333333", 
                font=ctk.CTkFont(size=16, weight="bold")
            ).place(relx=0.5, rely=0.5, anchor="center")
            
        # -------------------- 2. Right Frame (Registration Form Panel - 50% of screen) --------------------
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent") 
        self.form_frame.grid(row=0, column=1, sticky="nsew")
        
        # Inner frame to contain and center the form widgets using relative positioning
        form_center_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        form_center_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center using relative positioning
        
        # ---- Titles ----
        ctk.CTkLabel(
            form_center_frame, 
            text="🛒 Smart Inventory Management System", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF8C00"
        ).pack(pady=(10, 5))
        ctk.CTkLabel(
            form_center_frame, 
            text="Register", 
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(5, 25))
        
        # ---- Input Fields ----
        self.create_field(form_center_frame, "First Name:")
        self.create_field(form_center_frame, "Last Name:")
        self.create_field(form_center_frame, "Email:")
        self.create_field(form_center_frame, "Phone Number:")
        # Password fields now have the toggle logic inside create_field
        self.create_field(form_center_frame, "Password:", is_password=True)
        self.create_field(form_center_frame, "Confirm Password:", is_password=True)
        
        # ---- Register as ----
        row = ctk.CTkFrame(form_center_frame, fg_color="transparent")
        row.pack(pady=(10, 10))
        role_label = ctk.CTkLabel(
            row, text="Register as:", font=ctk.CTkFont(size=14), width=150, anchor="e"
        )
        role_label.pack(side="left", padx=(0, 10))
        radio_frame = ctk.CTkFrame(row, fg_color="transparent")
        radio_frame.pack(side="left")
        self.user_type_var = tk.StringVar(value="customer")
        ctk.CTkRadioButton(
            radio_frame,
            text="Customer",
            variable=self.user_type_var,
            value="customer",
            font=ctk.CTkFont(size=13),
        ).pack(side="left", padx=10)
        ctk.CTkRadioButton(
            radio_frame,
            text="Staff",
            variable=self.user_type_var,
            value="staff",
            font=ctk.CTkFont(size=13),
        ).pack(side="left", padx=10)
        
        # ---- Register Button ----
        register_button = ctk.CTkButton(
            form_center_frame,
            text="Register",
            width=200,
            height=45,
            font=ctk.CTkFont(size=16),
            command=self.register,
        )
        register_button.pack(pady=(30, 15))
        
        # ---- Login link ----
        login_frame = ctk.CTkFrame(form_center_frame, fg_color="transparent")
        login_frame.pack(pady=(10, 10))
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account?",
            font=ctk.CTkFont(size=14),
        )
        login_label.pack(side="left")
        
        login_link = ctk.CTkButton(
            login_frame,
            text="Login",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover=False,
            text_color="#FF8C00",
            command=self.open_login
        )
        login_link.pack(side="left", padx=(5, 0))
        
        # ---- Back to Home Button ----
        back_button = ctk.CTkButton(
            form_center_frame,
            text="← Back to Home",
            width=200,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            command=self.back_to_home
        )
        back_button.pack(pady=(10, 10))
        
        # Set focus to first name entry
        self.first_name_entry.focus_set()
        
        # macOS focus fix
        self.after(150, self._bring_to_front)
    
    def _toggle_password_visibility(self, entry):
        """Toggle password visibility"""
        current_show = entry.cget("show")
        if current_show == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")
    
    def create_field(self, parent, label_text, is_password=False):
        """Helper: creates a horizontal label + entry row with optional password toggle."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(pady=(5, 10))
        
        label = ctk.CTkLabel(
            row, text=label_text, font=ctk.CTkFont(size=14), width=150, anchor="e"
        )
        label.pack(side="left", padx=(0, 10))
        
        entry_width = 400
        show_char = "*" if is_password else ""
        
        if is_password:
            # Reduce entry width to make space for the toggle button
            entry_width = 350
            
            entry = ctk.CTkEntry(row, width=entry_width, height=40, show=show_char)
            entry.pack(side="left")
            
            # Create and pack the toggle button
            toggle_button = ctk.CTkButton(
                row,
                text="👁", # Eye emoji for visibility toggle
                width=40,
                height=40,
                corner_radius=8,
                command=lambda e=entry: self._toggle_password_visibility(e)
            )
            toggle_button.pack(side="left", padx=(5, 0))
            
            # Store reference to password entries
            if "Password:" in label_text and "Confirm" not in label_text:
                self.password_entry = entry
            elif "Confirm Password:" in label_text:
                self.confirm_password_entry = entry
        else:
            entry = ctk.CTkEntry(row, width=entry_width, height=40, show=show_char)
            entry.pack(side="left")
            
            # Store reference to other entries
            if "First Name:" in label_text:
                self.first_name_entry = entry
            elif "Last Name:" in label_text:
                self.last_name_entry = entry
            elif "Email:" in label_text:
                self.email_entry = entry
            elif "Phone Number:" in label_text:
                self.phone_entry = entry
    
    def _resize_image(self, label, img):
        """Resize image to fit the frame properly"""
        try:
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()
            if frame_width > 1 and frame_height > 1:
                # Resize image to fit frame
                resized_img = img.resize((frame_width, frame_height), Image.LANCZOS)
                self.bg_image = ctk.CTkImage(light_image=resized_img, dark_image=resized_img, size=(frame_width, frame_height))
                label.configure(image=self.bg_image)
        except Exception:
            pass
    
    def _bring_to_front(self):
        try:
            self.lift()
            self.focus_force()
            self.attributes("-topmost", True)
            self.after(120, lambda: self.attributes("-topmost", False))
        except Exception:
            pass
    
    def back_to_home(self):
        """Return to home screen"""
        self.destroy()
        if hasattr(self.master, 'deiconify'):
            self.master.deiconify()
        if hasattr(self.master, 'create_home_screen'):
            self.master.create_home_screen()
    
    def hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        user_type = self.user_type_var.get()
        
        # Validate inputs
        if not first_name or not last_name or not email or not phone or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Validate first name and last name (alphabetic only)
        if not first_name.replace(' ', '').isalpha():
            messagebox.showerror("Error", "First name should contain only letters")
            return
        
        if not last_name.replace(' ', '').isalpha():
            messagebox.showerror("Error", "Last name should contain only letters")
            return
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        # Validate phone number (numbers, spaces, hyphens, parentheses)
        phone_cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        if not phone_cleaned.isdigit() or len(phone_cleaned) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number (at least 10 digits)")
            return
        
        # Validate password strength - check all requirements first
        password_errors = []
        
        if len(password) < 8:
            password_errors.append("• At least 8 characters long")
        
        if not any(c.isupper() for c in password):
            password_errors.append("• At least one uppercase letter (A-Z)")
        
        if not any(c.islower() for c in password):
            password_errors.append("• At least one lowercase letter (a-z)")
        
        if not any(c.isdigit() for c in password):
            password_errors.append("• At least one number (0-9)")
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            password_errors.append("• At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
        
        # Show all validation errors in one message
        if password_errors:
            error_message = "Password must contain:\n\n" + "\n".join(password_errors)
            messagebox.showerror("Password Requirements", error_message)
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
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
                    "INSERT INTO users (first_name, last_name, email, phone_number, password, user_type, is_approved) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, email, phone, self.hash_password(password), user_type, is_approved)
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
