from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

from services.auth_service import auth_service


class LoginPage(ctk.CTkFrame):

    def __init__(self, master, on_login, on_show_register):
        super().__init__(master)

        self.on_login = on_login
        self.on_show_register = on_show_register

        self.build_ui()

    def build_ui(self):

        self.pack(fill="both", expand=True)

        container = ctk.CTkFrame(
            self,
            width=550,
            height=500,
            corner_radius=20
        )

        container.pack(expand=True)
        container.pack_propagate(False)

        title = ctk.CTkLabel(
            container,
            text="SkillSwap",
            font=ctk.CTkFont(size=34, weight="bold")
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            container,
            text="Login to continue",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(pady=(0, 30))

        self.email_entry = ctk.CTkEntry(
            container,
            placeholder_text="Email",
            width=420,
            height=45
        )
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Password",
            show="*",
            width=420,
            height=45
        )
        self.password_entry.pack(pady=10)

        login_btn = ctk.CTkButton(
            container,
            text="Login",
            width=420,
            height=45,
            command=self.login
        )
        login_btn.pack(pady=(25, 10))

        # register_btn = ctk.CTkButton(
        #     container,
        #     text="Create Account",
        #     width=420,
        #     height=45,
        #     fg_color="transparent",
        #     border_width=2,
        #     command=self.on_show_register
        # )
        # register_btn.pack()

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    def login(self):

        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter email and password."
            )
            return

        user = auth_service.login(
            email,
            password
        )

        if user is None:

            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )
            return

        self.on_login(user)