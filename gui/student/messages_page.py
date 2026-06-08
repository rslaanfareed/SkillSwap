import customtkinter as ctk
from tkinter import messagebox

from services.student_service import student_service


class MessagesPage(ctk.CTkFrame):

    def __init__(
        self,
        master,
        user,
        session_id
    ):
        super().__init__(master)

        self.user = user
        self.session_id = session_id

        self.build_ui()

        self.refresh_messages()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text=f"Session Chat #{self.session_id}",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            pady=20
        )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20
        )

        ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.refresh_messages
        ).pack(
            side="left",
            padx=5
        )

        self.messages_box = ctk.CTkTextbox(
            self,
            height=400
        )

        self.messages_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        input_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.message_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type a message..."
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message
        ).pack(
            side="right"
        )

    def refresh_messages(self):

        student_service.mark_messages_read(
            self.session_id,
            self.user["user_id"]
        )

        messages = student_service.get_session_messages(
            self.session_id
        )

        self.messages_box.delete(
            "1.0",
            "end"
        )

        for msg in messages:

            sender_id = msg[1]
            sender_name = msg[2]
            content = msg[3]
            sent_at = msg[4]

            if sender_id == self.user["user_id"]:

                self.messages_box.insert(
                    "end",
                    f"\nMe ({sent_at})\n{content}\n"
                )

            else:

                self.messages_box.insert(
                    "end",
                    f"\n{sender_name} ({sent_at})\n{content}\n"
                )

    def send_message(self):

        text = self.message_entry.get()

        success = student_service.send_message(
            self.session_id,
            self.user["user_id"],
            text
        )

        if not success:

            messagebox.showerror(
                "Error",
                "Failed to send message."
            )

            return

        self.message_entry.delete(
            0,
            "end"
        )

        self.refresh_messages()