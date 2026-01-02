import os
import customtkinter as ctk
from PIL import Image, ImageTk
import db_config

# Set appearance mode and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
ctk.ThemeManager.theme["CTkButton"]["fg_color"] = ["#FF8C00", "#FF6500"]
ctk.ThemeManager.theme["CTkButton"]["hover_color"] = ["#FF6500", "#FF4500"]

class InventoryManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Inventory Management System")
        # Make full screen and resizable
        self.state('zoomed')  # Windows full screen
        self.resizable(True, True)

        # Load icon
        try:
            iconpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "logo1.png")
            self.iconphoto(False, ImageTk.PhotoImage(Image.open(iconpath)))
        except:
            pass

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.current_user = None
        self.create_home_screen()

    # ---------------- HOME SCREEN ----------------
    def create_home_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 40))

        # Logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "logo1.png")
            logo_image = Image.open(logo_path).resize((100, 100))
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.image = logo_photo
            logo_label.pack(side="left", padx=(0, 20))
        except:
            pass

        title_label = ctk.CTkLabel(header_frame, text="Smart Inventory Management System",
                                   font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(side="left", padx=20)

        # Content
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="#febd6e")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Hero Image
        try:
            hero_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "cat2.png")
            hero_image = Image.open(hero_path).resize((400, 300))
            hero_photo = ImageTk.PhotoImage(hero_image)
            hero_label = ctk.CTkLabel(content_frame, image=hero_photo, text="")
            hero_label.image = hero_photo
            hero_label.pack(pady=(40, 20))
        except:
            pass

        ctk.CTkLabel(content_frame, text="Welcome to SIMS", text_color="black",
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(content_frame, text="Manage your inventory, track orders, and monitor sales with ease.", text_color="black",
                     font=ctk.CTkFont(size=16)).pack(pady=(0, 30))

        # Buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        ctk.CTkButton(buttons_frame, text="Login", font=ctk.CTkFont(size=18), width=220, height=55,
                      command=self.open_login).pack(side="left", padx=20)
        ctk.CTkButton(buttons_frame, text="Register", font=ctk.CTkFont(size=18), width=220, height=55,
                      command=self.open_register).pack(side="left", padx=20)

        # Footer
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=40)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        ctk.CTkLabel(footer_frame, text="© 2024 Smart Inventory Management System",
                     font=ctk.CTkFont(size=12)).pack(side="right")

    # ---------------- OPEN LOGIN ----------------
    def open_login(self):
        # Clear main frame (destroy current page)
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Hide main window and open login screen
        self.withdraw()
        from login_screen import LoginScreen
        login_window = LoginScreen(self)
        login_window.grab_set()

    # ---------------- OPEN REGISTER ----------------
    def open_register(self):
        # Clear main frame (destroy current page)
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Hide main window and open registration screen
        self.withdraw()
        from user_registration import RegisterScreen
        register_window = RegisterScreen(self)
        register_window.grab_set()

    def login_success(self, user_data):
        # Add full_name to user_data if not present (for compatibility with older code)
        if 'full_name' not in user_data:
            user_data['full_name'] = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
        
        self.current_user = user_data
        # Show main window and navigate to appropriate dashboard
        self.deiconify()
        
        # Clear main frame first
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Import and navigate to appropriate dashboard based on user type
        if user_data['user_type'] == 'admin':
            from admin_dashboard import AdminDashboard
            self.current_dashboard = AdminDashboard(self.main_frame, self)
        elif user_data['user_type'] == 'customer':
            from customer_dashboard import CustomerDashboard
            self.current_dashboard = CustomerDashboard(self.main_frame, self)
        elif user_data['user_type'] == 'staff':
            from staff_dashboard import StaffDashboard
            self.current_dashboard = StaffDashboard(self.main_frame, self)
        else:
            # Unknown user type - return to home
            self.create_home_screen()
    
    def logout(self):
        """Logout user and return to home screen"""
        # Clear current user
        self.current_user = None
        
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Close database connection if dashboard has one
        if hasattr(self, 'current_dashboard') and hasattr(self.current_dashboard, 'db_connection'):
            if self.current_dashboard.db_connection and self.current_dashboard.db_connection.is_connected():
                self.current_dashboard.db_connection.close()
        
        # Clear dashboard reference
        if hasattr(self, 'current_dashboard'):
            del self.current_dashboard
        
        # Return to home screen
        self.create_home_screen()

if __name__ == "__main__":
    app = InventoryManagementSystem()
    app.mainloop()
