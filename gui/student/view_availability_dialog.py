import customtkinter as ctk


class ViewAvailabilityDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        availability
    ):

        super().__init__(parent)

        self.title(
            "Offer Availability"
        )

        self.geometry(
            "450x350"
        )

        self.build_ui(
            availability
        )

    def build_ui(
        self,
        availability
    ):

        ctk.CTkLabel(
            self,
            text="Availability Slots",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=15
        )

        frame = ctk.CTkScrollableFrame(
            self
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        if not availability:

            ctk.CTkLabel(
                frame,
                text="No availability added yet."
            ).pack(
                pady=20
            )

            return

        for day, slot in availability:

            card = ctk.CTkFrame(
                frame,
                border_width=1
            )

            card.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=f"{day}   |   {slot}",
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                padx=15,
                pady=10
            )