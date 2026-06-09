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
            hover_color="#cc0000",
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

        most_requested = (
            admin_service.get_most_requested_skill()
        )

        most_offered = (
            admin_service.get_most_offered_skill()
        )

        top_tutor = (
            admin_service.get_top_rated_tutor()
        )

        ctk.CTkLabel(
            self.content,
            text="Admin Dashboard",
            font=ctk.CTkFont(
                size=36,
                weight="bold"
            )
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            self.content,
            text="SkillSwap Analytics & Management",
            font=ctk.CTkFont(
                size=18
            )
        ).pack(
            pady=(0, 20)
        )

        stats_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        cards = [
            ("Users", stats["users"]),
            ("Departments", stats["departments"]),
            ("Skills", stats["skills"]),
            ("Suggestions", stats["suggestions"]),
            ("Offers", stats["offers"]),
            ("Requests", stats["requests"]),
            ("Sessions", stats["sessions"]),
            ("Pending", stats["pending_requests"])
        ]

        for i, (title, value) in enumerate(cards):

            card = ctk.CTkFrame(
                stats_frame,
                corner_radius=15,
                border_width=2
            )

            card.grid(
                row=i // 4,
                column=i % 4,
                padx=12,
                pady=12,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(
                    size=18
                )
            ).pack(
                pady=(20, 8)
            )

            ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(
                    size=34,
                    weight="bold"
                )
            ).pack(
                pady=(0, 20)
            )

        for col in range(4):
            stats_frame.grid_columnconfigure(
                col,
                weight=1,
                minsize=220
            )




        analytics_frame = ctk.CTkFrame(
            self.content,
            corner_radius=15,
            border_width=2
        )

        analytics_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        ctk.CTkLabel(
            analytics_frame,
            text="Platform Insights",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(15, 20)
        )

        insights = [
    f"🔥 Most Requested Skill: {most_requested}",
    f"📚 Most Offered Skill: {most_offered}",
    f"⭐ Top Rated Tutor: {top_tutor}",
    f"📈 Total Offers: {stats['offers']}",
    f"📝 Total Requests: {stats['requests']}",
    f"📅 Total Sessions: {stats['sessions']}",
    
]

        for item in insights:

            ctk.CTkLabel(
                analytics_frame,
                text=item,
                anchor="w",
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                anchor="w",
                padx=25,
                pady=6
            )

    

   

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