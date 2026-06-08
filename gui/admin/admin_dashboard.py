import customtkinter as ctk

from services.admin_service import admin_service

from gui.admin.users_page import UsersPage
from gui.admin.skills_page import SkillsPage
from gui.admin.suggestions_page import SuggestionsPage


class AdminDashboard(ctk.CTkFrame):

    def __init__(self, master, user, on_logout):
        super().__init__(master)

        self.user = user
        self.on_logout = on_logout

        self.pack(
            fill="both",
            expand=True
        )

        self.build_ui()

    def build_ui(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="SkillSwap",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            pady=(30, 10)
        )

        ctk.CTkLabel(
            self.sidebar,
            text=f"Admin\n{self.user['name']}",
            justify="center",
            font=ctk.CTkFont(
                size=18
            )
        ).pack(
            pady=(0, 25)
        )

        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Users",
            command=self.show_users,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Skills",
            command=self.show_skills,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Suggestions",
            command=self.show_suggestions,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="red",
            command=self.on_logout,
            height=40
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        self.content = ctk.CTkFrame(self)

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def add_theme_button(self):

        ctk.CTkButton(
            self.content,
            text="Dark/Light",
            width=120,
            height=36,
            command=self.winfo_toplevel().toggle_theme
        ).place(
            relx=0.98,
            y=20,
            anchor="ne"
        )

    def show_dashboard(self):

        self.clear_content()

        self.add_theme_button()

        stats = admin_service.get_dashboard_stats()

        ctk.CTkLabel(
            self.content,
            text="Admin Dashboard",
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            )
        ).pack(
            pady=25
        )

        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards_frame.pack(
            pady=30
        )

        self.create_card(
            cards_frame,
            "Users",
            stats["users"],
            0
        )

        self.create_card(
            cards_frame,
            "Departments",
            stats["departments"],
            1
        )

        self.create_card(
            cards_frame,
            "Skills",
            stats["skills"],
            2
        )

        self.create_card(
            cards_frame,
            "Suggestions",
            stats["suggestions"],
            3
        )

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            width=220,
            height=140
        )

        card.grid(
            row=0,
            column=column,
            padx=20
        )

        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=20
            )
        ).pack(
            pady=(25, 10)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(
                size=36,
                weight="bold"
            )
        ).pack()

    def show_users(self):

        self.clear_content()

        self.add_theme_button()

        page = UsersPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

    def show_skills(self):

        self.clear_content()

        self.add_theme_button()

        page = SkillsPage(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )

    def show_suggestions(self):

        self.clear_content()

        self.add_theme_button()

        page = SuggestionsPage(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )