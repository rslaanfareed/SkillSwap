import customtkinter as ctk


class OfferDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        skills,
        offer_data=None
    ):
        super().__init__(parent)

        self.title("Offer")

        self.geometry("450x350")

        self.resizable(
            False,
            False
        )

        self.result = None

        self.skills = skills

        ctk.CTkLabel(
            self,
            text="Offer Details",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(20, 10)
        )

        ctk.CTkLabel(
            self,
            text="Skill"
        ).pack(
            anchor="w",
            padx=30
        )

        self.skill_menu = ctk.CTkComboBox(
            self,
            values=[
                skill[1]
                for skill in skills
            ],
            width=350
        )

        self.skill_menu.pack(
            padx=30,
            pady=(5, 15)
        )

        ctk.CTkLabel(
            self,
            text="Level"
        ).pack(
            anchor="w",
            padx=30
        )

        self.level_menu = ctk.CTkComboBox(
            self,
            values=[
                "BEGINNER",
                "INTERMEDIATE",
                "EXPERT"
            ],
            width=350
        )

        self.level_menu.pack(
            padx=30,
            pady=(5, 15)
        )

        ctk.CTkLabel(
            self,
            text="Session Mode"
        ).pack(
            anchor="w",
            padx=30
        )

        self.mode_menu = ctk.CTkComboBox(
            self,
            values=[
                "ONLINE",
                "IN_PERSON",
                "BOTH"
            ],
            width=350
        )

        self.mode_menu.pack(
            padx=30,
            pady=(5, 20)
        )

        if offer_data:

            self.skill_menu.set(
                offer_data["skill_name"]
            )

            self.level_menu.set(
                offer_data["level"]
            )

            self.mode_menu.set(
                offer_data["mode"]
            )

        else:

            self.skill_menu.set(
                skills[0][1]
            )

            self.level_menu.set(
                "BEGINNER"
            )

            self.mode_menu.set(
                "ONLINE"
            )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=10
        )

        ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(
            side="left",
            padx=10
        )

        self.grab_set()

    def save(self):

        skill_name = self.skill_menu.get()

        skill_id = None

        for skill in self.skills:

            if skill[1] == skill_name:

                skill_id = skill[0]
                break

        self.result = (
            skill_id,
            self.level_menu.get(),
            self.mode_menu.get()
        )

        self.destroy()