import customtkinter as ctk


class RequestDialog(ctk.CTkToplevel):

    def __init__(self, parent, availability_list):
        super().__init__(parent)

        self.title("Request Skill")
        self.geometry("500x450")

        self.result = None

        self.availability_list = availability_list

        self.grab_set()

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Create Request",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=15
        )

        ctk.CTkLabel(
            self,
            text="Availability"
        ).pack(
            pady=(10, 5)
        )

        availability_values = []

        for row in self.availability_list:

            availability_values.append(
                f"{row[1]} - {row[2]}"
            )

        self.availability_menu = ctk.CTkOptionMenu(
            self,
            values=availability_values
        )

        self.availability_menu.pack(
            padx=20,
            fill="x"
        )

        ctk.CTkLabel(
            self,
            text="Urgency"
        ).pack(
            pady=(15, 5)
        )

        self.urgency_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "LOW",
                "MEDIUM",
                "HIGH"
            ]
        )

        self.urgency_menu.pack(
            padx=20,
            fill="x"
        )

        ctk.CTkLabel(
            self,
            text="Note (Optional)"
        ).pack(
            pady=(15, 5)
        )

        self.note_box = ctk.CTkTextbox(
            self,
            height=120
        )

        self.note_box.pack(
            padx=20,
            fill="both"
        )

        ctk.CTkButton(
            self,
            text="Submit Request",
            command=self.submit
        ).pack(
            pady=20
        )

    def submit(self):

        selected_index = (
            self.availability_menu.cget(
                "values"
            ).index(
                self.availability_menu.get()
            )
        )

        availability_id = (
            self.availability_list[selected_index][0]
        )

        urgency = self.urgency_menu.get()

        note = self.note_box.get(
            "1.0",
            "end"
        ).strip()

        self.result = (
            availability_id,
            urgency,
            note
        )

        self.destroy()