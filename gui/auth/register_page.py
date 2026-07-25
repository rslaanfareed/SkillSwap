import re
import customtkinter as ctk
from tkinter import messagebox

from services.auth_service import auth_service


class RegisterPage(ctk.CTkFrame):

    def __init__(self, master, on_back):
        super().__init__(master)

        self.on_back = on_back

        self.departments = (
            auth_service.get_departments()
        )

        self.build_ui()

    def build_ui(self):

        self.pack(
            fill="both",
            expand=True
        )

        container = ctk.CTkFrame(
            self,
            width=650,
            height=700,
            corner_radius=20
        )

        container.pack(
            expand=True,
            pady=20
        )

        container.pack_propagate(False)

        ctk.CTkLabel(
            container,
            text="Create Account",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        ).pack(
            pady=(30, 20)
        )

        self.name_entry = ctk.CTkEntry(
            container,
            placeholder_text="Full Name",
            width=450
        )

        self.name_entry.pack(
            pady=8
        )

        department_names = [
            dept[1]
            for dept in self.departments
        ]

        self.department_menu = ctk.CTkOptionMenu(
            container,
            values=department_names,
            width=450
        )

        self.department_menu.pack(
            pady=8
        )

        self.batch_entry = ctk.CTkEntry(
            container,
            placeholder_text="Batch (Example: 2024)",
            width=450
        )

        self.batch_entry.pack(
            pady=8
        )

        self.email_entry = ctk.CTkEntry(
            container,
            placeholder_text="Email",
            width=450
        )

        self.email_entry.pack(
            pady=8
        )

        self.phone_entry = ctk.CTkEntry(
            container,
            placeholder_text="Phone Number (03XXXXXXXXX)",
            width=450
        )

        self.phone_entry.pack(
            pady=8
        )

        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Password",
            show="*",
            width=450
        )

        self.password_entry.pack(
            pady=8
        )

        self.confirm_entry = ctk.CTkEntry(
            container,
            placeholder_text="Confirm Password",
            show="*",
            width=450
        )

        self.confirm_entry.pack(
            pady=8
        )

        ctk.CTkButton(
            container,
            text="Register",
            width=450,
            height=42,
            command=self.register
        ).pack(
            pady=(20, 10)
        )

        ctk.CTkButton(
            container,
            text="Back to Login",
            width=450,
            height=42,
            fg_color="transparent",
            border_width=2,
            command=self.on_back
        ).pack()

    def register(self):

        name = self.name_entry.get().strip()
        batch = self.batch_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not all([
            name,
            batch,
            email,
            phone,
            password,
            confirm
        ]):

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        if len(name) < 3:

            messagebox.showerror(
                "Invalid Name",
                "Name must contain at least 3 characters."
            )

            return

        if not re.fullmatch(
            r"[A-Za-z]+(?: [A-Za-z]+)*",
            name
        ):

            messagebox.showerror(
                "Invalid Name",
                "Please enter a valid full name using letters only."
            )

            return

        if not batch.isdigit():

            messagebox.showerror(
                "Invalid Batch",
                "Batch must contain only numbers.\nExample: 2024"
            )

            return

        batch = int(batch)

        if batch < 2015 or batch > 2035:

            messagebox.showerror(
                "Invalid Batch",
                "Please enter a valid batch year."
            )

            return

        email_pattern = (
            r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        if not re.match(
            email_pattern,
            email
        ):

            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address."
            )

            return

        if auth_service.email_exists(email):

            messagebox.showerror(
                "Email Exists",
                "An account with this email already exists."
            )

            return

        if not phone.isdigit():

            messagebox.showerror(
                "Invalid Phone Number",
                "Phone number must contain digits only."
            )

            return

        if len(phone) != 11:

            messagebox.showerror(
                "Invalid Phone Number",
                "Phone number must be exactly 11 digits."
            )

            return

        if not phone.startswith("03"):

            messagebox.showerror(
                "Invalid Phone Number",
                "Phone number must start with 03."
            )

            return

        if len(password) < 8:

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least 8 characters."
            )

            return

        if not re.search(r"[A-Z]", password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least one uppercase letter."
            )

            return

        if not re.search(r"[a-z]", password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least one lowercase letter."
            )

            return

        if not re.search(r"\d", password):

            messagebox.showerror(
                "Weak Password",
                "Password must contain at least one number."
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )

            return

        selected_department = (
            self.department_menu.get()
        )

        department_id = None

        for dept in self.departments:

            if dept[1] == selected_department:

                department_id = dept[0]
                break

        success = auth_service.register_student(
            department_id,
            name,
            batch,
            email,
            phone,
            password
        )

        if success:

            messagebox.showinfo(
                "Account Created",
                "Your account has been created successfully.\nYou can now login."
            )

            self.on_back()

        else:

            messagebox.showerror(
                "Registration Failed",
                "Unable to create account.\nPlease try again."
            )