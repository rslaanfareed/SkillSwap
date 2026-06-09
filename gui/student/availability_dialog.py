import customtkinter as ctk


class AvailabilityDialog(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.result = None

        self.title("Add Availability")
        self.geometry("400x250")

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Availability Slot",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=20
        )

        self.day_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
                "SUNDAY"
            ]
        )

        self.day_menu.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.time_menu = ctk.CTkOptionMenu(
        self,
        values=[
            "MORNING",
            "AFTERNOON",
            "EVENING"
        ]
    )

        self.time_menu.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(
            pady=20
        )

    def save(self):

        self.result = (
            self.day_menu.get(),
            self.time_menu.get()
        )

        self.destroy()