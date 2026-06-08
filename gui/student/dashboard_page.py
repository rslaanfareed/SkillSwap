import customtkinter as ctk

from services.student_service import student_service


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.build_ui()

    def build_ui(self):

        stats = student_service.get_dashboard_stats(
            self.user["user_id"]
        )

        upcoming = student_service.get_upcoming_session(
            self.user["user_id"]
        )

        skills = student_service.get_my_skills(
            self.user["user_id"]
        )

        feedback = student_service.get_recent_feedback(
            self.user["user_id"]
        )

        ctk.CTkLabel(
            self,
            text=f"Welcome, {self.user['name']}",
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            )
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            self,
            text="Your SkillSwap Overview",
            font=ctk.CTkFont(size=16)
        ).pack(
            pady=(0, 20)
        )

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.create_card(
            stats_frame,
            "Offers",
            stats["offers"]
        ).pack(side="left", expand=True, padx=5)

        self.create_card(
            stats_frame,
            "Requests",
            stats["requests"]
        ).pack(side="left", expand=True, padx=5)

        self.create_card(
            stats_frame,
            "Sessions",
            stats["sessions"]
        ).pack(side="left", expand=True, padx=5)

        self.create_card(
            stats_frame,
            "Reviews",
            stats["reviews"]
        ).pack(side="left", expand=True, padx=5)

        self.create_card(
            stats_frame,
            "Rating",
            f"★ {stats['rating']}"
        ).pack(side="left", expand=True, padx=5)

        middle_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        middle_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        upcoming_card = ctk.CTkFrame(
            middle_frame,
            height=220
        )

        upcoming_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkLabel(
            upcoming_card,
            text="Upcoming Session",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=(15, 10)
        )

        if upcoming:

            ctk.CTkLabel(
                upcoming_card,
                text=f"Skill: {upcoming[0]}"
            ).pack(anchor="w", padx=20, pady=3)

            ctk.CTkLabel(
                upcoming_card,
                text=f"With: {upcoming[1]}"
            ).pack(anchor="w", padx=20, pady=3)

            ctk.CTkLabel(
                upcoming_card,
                text=f"Date: {upcoming[2]}"
            ).pack(anchor="w", padx=20, pady=3)

            ctk.CTkLabel(
                upcoming_card,
                text=f"Meeting: {upcoming[3]}"
            ).pack(anchor="w", padx=20, pady=3)

        else:

            ctk.CTkLabel(
                upcoming_card,
                text="No upcoming sessions."
            ).pack(
                pady=40
            )

        feedback_card = ctk.CTkFrame(
            middle_frame,
            height=220
        )

        feedback_card.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            feedback_card,
            text="Latest Feedback",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=(15, 10)
        )

        if feedback:

            ctk.CTkLabel(
                feedback_card,
                text=f"★ {feedback[0]}",
                font=ctk.CTkFont(
                    size=36,
                    weight="bold"
                )
            ).pack()

            ctk.CTkLabel(
                feedback_card,
                text=feedback[1],
                wraplength=350,
                justify="left"
            ).pack(
                padx=20,
                pady=10
            )

        else:

            ctk.CTkLabel(
                feedback_card,
                text="No feedback received yet."
            ).pack(
                pady=40
            )

        skills_card = ctk.CTkFrame(
            self
        )

        skills_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        ctk.CTkLabel(
            skills_card,
            text="My Skills",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=(15, 10)
        )

        if skills:

            for skill in skills:

                ctk.CTkLabel(
                    skills_card,
                    text=f"• {skill[0]}",
                    anchor="w"
                ).pack(
                    anchor="w",
                    padx=25,
                    pady=2
                )

        else:

            ctk.CTkLabel(
                skills_card,
                text="No skills offered yet."
            ).pack(
                pady=20
            )

    def create_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            width=180,
            height=120
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=16
            )
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack()

        return card