import customtkinter as ctk

from services.student_service import student_service


class NotificationsPage(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Notifications",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        ).pack(
            pady=(20, 10)
        )

        self.scroll = ctk.CTkScrollableFrame(
            self
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        notifications = (
            student_service.get_notifications(
                self.user["user_id"]
            )
        )

        if not notifications:

            ctk.CTkLabel(
                self.scroll,
                text="No notifications yet.",
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                pady=20
            )

            return

        for notification in notifications:

            card = ctk.CTkFrame(
                self.scroll,
                corner_radius=12
            )

            card.pack(
                fill="x",
                padx=10,
                pady=8
            )

            ctk.CTkLabel(
                card,
                text=notification[1],
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 5)
            )

            ctk.CTkLabel(
                card,
                text=notification[2]
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )