import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import date

class SessionDialog(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.result = None

        self.title("Schedule Session")
        self.geometry("500x350")

        self.grab_set()

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Schedule Session",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=20
        )

        ctk.CTkLabel(
            self,
            text="Session Date"
        ).pack()

        self.date_picker = DateEntry(
            self,
            date_pattern="yyyy-mm-dd",
            mindate=date.today(),
            width=25
        )

        self.date_picker.pack(
            padx=20,
            fill="x"
        )

        ctk.CTkLabel(
            self,
            text="Meeting Details"
        ).pack(
            pady=(15, 0)
        )

        self.details_box = ctk.CTkTextbox(
            self,
            height=120
        )

        self.details_box.pack(
            padx=20,
            fill="both",
            expand=True
        )

        ctk.CTkButton(
            self,
            text="Create Session",
            command=self.submit
        ).pack(
            pady=15
        )

    def submit(self):

        self.result = (
    self.date_picker.get(),
    self.details_box.get(
        "1.0",
        "end"
    ).strip()
)

        self.destroy()