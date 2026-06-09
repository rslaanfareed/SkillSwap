import customtkinter as ctk
from gui.student.sessions_page import SessionsPage
from gui.student.browse_skills_page import BrowseSkillsPage
from gui.student.offers_page import OffersPage
from gui.student.my_requests_page import MyRequestsPage
from gui.student.incoming_requests_page import IncomingRequestsPage
from gui.student.notifications_page import NotificationsPage

class StudentDashboard(ctk.CTkFrame):

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
            text=f"Student\n{self.user['name']}",
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
            text="My Offers",
            command=self.show_my_offers,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Browse Skills",
            command=self.show_browse_skills,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Incoming Requests",
            command=self.show_incoming_requests,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="My Requests",
            command=self.show_requests,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="My Sessions",
            command=self.show_sessions,
            height=40
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            self.sidebar,
            text="Notifications",
            command=self.show_notifications,
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
            width=130,
            height=36,
            command=self.winfo_toplevel().toggle_theme
        ).place(
            relx=0.98,
            y=20,
            anchor="ne"
        )

    def show_dashboard(self):

        self.clear_content()

        from gui.student.dashboard_page import DashboardPage

        page = DashboardPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.add_theme_button()

    def show_my_offers(self):

        self.clear_content()

        page = OffersPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )
        self.add_theme_button()


    def show_browse_skills(self):

        self.clear_content()

        

        page = BrowseSkillsPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )
        self.add_theme_button()
    
    def show_incoming_requests(self):

        self.clear_content()

        page = IncomingRequestsPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.add_theme_button()
    
    def show_requests(self):

        self.clear_content()

        

        page = MyRequestsPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )
        self.add_theme_button()


    def show_notifications(self):

        self.clear_content()

        page = NotificationsPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.add_theme_button()


    def show_sessions(self):

        self.clear_content()

        page = SessionsPage(
            self.content,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )

        self.add_theme_button()

   