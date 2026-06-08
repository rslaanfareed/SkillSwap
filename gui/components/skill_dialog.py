import customtkinter as ctk


class SkillDialog(ctk.CTkToplevel):

    def __init__(self, parent, categories):
        super().__init__(parent)

        self.result = None

        self.title("Add Skill")
        self.geometry("450x350")
        self.resizable(False, False)

        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Add New Skill",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self,
            text="Skill Name"
        ).pack(anchor="w", padx=30)

        self.skill_entry = ctk.CTkEntry(
            self,
            width=350,
            height=40
        )
        self.skill_entry.pack(padx=30, pady=(5, 15))

        ctk.CTkLabel(
            self,
            text="Category"
        ).pack(anchor="w", padx=30)

        category_names = [
            f"{row[0]} - {row[1]}"
            for row in categories
        ]

        self.category_menu = ctk.CTkComboBox(
            self,
            values=category_names,
            width=350,
            height=40
        )

        if category_names:
            self.category_menu.set(
                category_names[0]
            )

        self.category_menu.pack(
            padx=30,
            pady=(5, 25)
        )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_frame.pack()

        ctk.CTkButton(
            button_frame,
            text="Add",
            width=120,
            command=self.submit
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            fg_color="gray",
            command=self.destroy
        ).pack(
            side="left",
            padx=10
        )

    def submit(self):

        skill_name = self.skill_entry.get().strip()

        if not skill_name:
            return

        category_id = int(
            self.category_menu.get().split(" - ")[0]
        )

        self.result = (
            skill_name,
            category_id
        )

        self.destroy()