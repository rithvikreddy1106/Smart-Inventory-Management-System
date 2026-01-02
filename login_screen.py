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
        
        self.title("Smart Inventory Management System - Login")
        # Make full screen and resizable
        self.state('zoomed')  # Windows full screen
        self.resizable(True, True)
        
        # -------------------- Main Container Frame (50/50 split) --------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Configure grid for two equal columns: 0 (image), 1 (form)
        self.main_frame.grid_columnconfigure(0, weight=1) 
        self.main_frame.grid_columnconfigure(1, weight=1) 
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # -------------------- 1. Left Frame (Image - 50% of screen) --------------------
        self.image_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFE5B4")  # Light orange background
        self.image_frame.grid(row=0, column=0, sticky="nsew")
        
        # --- Load and Display bg.png Image ---
        try:
            bg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "bg.png")
            if not os.path.exists(bg_path):
                bg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "background.png")
            
            # Load image and create CTkImage for better scaling
            img = Image.open(bg_path)
            # Use CTkImage for better HighDPI support
            self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
            
            # Use CTkLabel to display the image
            image_label = ctk.CTkLabel(self.image_frame, image=self.bg_image, text="")
            image_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the image
            
        except Exception as e:
            print(f"Could not load side image: {e}")
            ctk.CTkLabel(
                self.image_frame, 
                text="Smart Inventory", 
                text_color="white", 
                fg_color="#2c3e50",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(expand=True)
            
        # -------------------- 2. Right Frame (Login Form Panel - 50% of screen) --------------------
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
            text="Login", 
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(5, 25))
        
        # ---- Input Fields ----
        self.create_field(form_center_frame, "Email:")
        self.create_field(form_center_frame, "Password:", is_password=True)
        
        # ---- Login Button ----
        login_button = ctk.CTkButton(
            form_center_frame,
            text="Login",
            width=200,
            height=45,
            font=ctk.CTkFont(size=16),
            command=self.login,
        )
        login_button.pack(pady=(30, 15))
        
        # ---- Register link ----
        register_frame = ctk.CTkFrame(form_center_frame, fg_color="transparent")
        register_frame.pack(pady=(10, 10))
        
        register_label = ctk.CTkLabel(
            register_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(size=14),
        )
        register_label.pack(side="left")
        
        register_link = ctk.CTkButton(
            register_frame,
            text="Register",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover=False,
            text_color="#FF8C00",
            command=self.open_register
        )
        register_link.pack(side="left", padx=(5, 0))
        
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
        
        # Set focus to email entry
        self.email_entry.focus_set()
        
        # Bind Enter key to login
        self.bind("<Return>", lambda event: self.login())
        
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
            
            # Store reference to password entry
            self.password_entry = entry
        else:
            entry = ctk.CTkEntry(row, width=entry_width, height=40, show=show_char)
            entry.pack(side="left")
            
            # Store reference to email entry
            self.email_entry = entry
    
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
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Please enter a valid email address")
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
                    
                    # Add full_name to user dict for compatibility
                    if 'full_name' not in user:
                        user['full_name'] = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
                    
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
        """Open registration screen"""
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
            # Add full_name if not present
            if 'full_name' not in user_data:
                user_data['full_name'] = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
            
            messagebox.showinfo("Login Successful", 
                f"Welcome, {user_data['full_name']}!\n\n"
                f"User Type: {user_data['user_type'].capitalize()}\n\n"
                f"Note: This is standalone mode.\n"
                f"Run main.py for the full application.")
            self.destroy()
    
    app = StandaloneApp()
    app.mainloop()
