import customtkinter as ctk
from tkinter import ttk, messagebox
from gui.student.messages_page import MessagesPage
from gui.student.feedback_dialog import FeedbackDialog
from services.student_service import student_service


class SessionsPage(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.tree = None
        self.selected_session_id = None

        self.build_ui()

    def build_ui(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=35,
            font=("Segoe UI", 11),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#202020",
            foreground="white",
            font=("Segoe UI", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#1f6aa5")
            ]
        )

        ctk.CTkLabel(
            self,
            text="My Sessions",
            font=ctk.CTkFont(
                size=32,
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
            text="Confirm Session",
            command=self.confirm_session
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Complete Session",
            command=self.complete_session
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.refresh_table
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Open Chat",
            command=self.open_chat
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Give Feedback",
            command=self.give_feedback
        ).pack(
            side="left",
            padx=5
        )

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "Session ID",
            "Skill",
            "Participant",
            "Date",
            "Status",
            "Meeting Details"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.heading(
            "Session ID",
            text="Session ID"
        )

        self.tree.heading(
            "Skill",
            text="Skill"
        )

        self.tree.heading(
            "Participant",
            text="Participant"
        )

        self.tree.heading(
            "Date",
            text="Date"
        )

        self.tree.heading(
            "Status",
            text="Status"
        )

        self.tree.heading(
            "Meeting Details",
            text="Meeting Details"
        )

        self.tree.column(
            "Session ID",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Skill",
            width=180
        )

        self.tree.column(
            "Participant",
            width=180
        )

        self.tree.column(
            "Date",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Status",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Meeting Details",
            width=400
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_session_selected
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.refresh_table()

    def refresh_table(self):

        self.selected_session_id = None

        for row in self.tree.get_children():
            self.tree.delete(row)

        sessions = student_service.get_my_sessions(
            self.user["user_id"]
        )

        for session in sessions:

            self.tree.insert(
                "",
                "end",
                values=session
            )

    def on_session_selected(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_session_id = values[0]

    def confirm_session(self):

        if self.selected_session_id is None:

            messagebox.showwarning(
                "Select Session",
                "Please select a session first."
            )

            return

        success = student_service.confirm_session(
            self.selected_session_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Session confirmed."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to confirm session."
            )

        self.refresh_table()

    def complete_session(self):

        if self.selected_session_id is None:

            messagebox.showwarning(
                "Select Session",
                "Please select a session first."
            )

            return

        success = student_service.complete_session(
            self.selected_session_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Session marked as completed."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to complete session."
            )

        self.refresh_table()

    def open_chat(self):

        if self.selected_session_id is None:

            messagebox.showwarning(
                "Select Session",
                "Please select a session first."
            )

            return

        self.destroy()

        page = MessagesPage(
            self.master,
            self.user,
            self.selected_session_id
        )

        page.pack(
            fill="both",
            expand=True
        )

    def give_feedback(self):

        if self.selected_session_id is None:

            messagebox.showwarning(
                "Select Session",
                "Please select a session first."
            )

            return

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        status = values[4]
        requester_id = values[6]

        if status != "COMPLETED":

            messagebox.showwarning(
                "Not Allowed",
                "Only completed sessions can be rated."
            )

            return

        if requester_id != self.user["user_id"]:

            messagebox.showwarning(
                "Not Allowed",
                "Only the requester can submit feedback."
            )

            return

        if student_service.has_feedback(
            self.selected_session_id
        ):

            messagebox.showwarning(
                "Feedback Exists",
                "Feedback already submitted."
            )

            return

        def submit_feedback(
            score,
            feedback_text
        ):

            success = student_service.add_feedback(
                self.selected_session_id,
                score,
                feedback_text
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Feedback submitted successfully."
                )

                self.refresh_table()

            else:

                messagebox.showerror(
                    "Error",
                    "Failed to submit feedback."
                )

        FeedbackDialog(
            self,
            submit_feedback
        )