import customtkinter as ctk
from gui.auth.register_page import RegisterPage
from gui.auth.login_page import LoginPage
from gui.admin.admin_dashboard import AdminDashboard
from gui.student.student_dashboard import StudentDashboard


class SkillSwapApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.current_theme = "dark"
        self.title("SkillSwap")
        
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.current_page = None

        self.show_login()

    def clear_page(self):

        if self.current_page is not None:
            self.current_page.destroy()
            self.current_page = None
    
    def toggle_theme(self):

        if self.current_theme == "dark":

            self.current_theme = "light"
            ctk.set_appearance_mode("light")

        else:

            self.current_theme = "dark"
            ctk.set_appearance_mode("dark")
    def show_login(self):

        self.clear_page()

        self.current_page = LoginPage(
            self,
            self.handle_login,
            self.show_register
        )

    def show_register(self):

        self.clear_page()

        self.current_page = RegisterPage(
            self,
            self.show_login
        )

    def handle_login(self, user):

        print("\nLOGIN SUCCESS")
        print(user)

        self.clear_page()

        if user["role"] == "ADMIN":

            self.current_page = AdminDashboard(
                self,
                user,
                self.show_login
            )

        elif user["role"] == "STUDENT":

            self.current_page = StudentDashboard(
                self,
                user,
                self.show_login
            )

        else:

            label = ctk.CTkLabel(
                self,
                text=f"Unknown Role\n\n{user['role']}",
                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )
            )

            label.pack(
                expand=True,
                fill="both"
            )

            self.current_page = label


if __name__ == "__main__":

    app = SkillSwapApp()
    app.mainloop()