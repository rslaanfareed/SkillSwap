from gui.student.session_dialog import SessionDialog
import customtkinter as ctk
from tkinter import ttk, messagebox

from services.student_service import student_service


class IncomingRequestsPage(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.tree = None
        self.selected_request_id = None

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
            text="Incoming Requests",
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
            text="Accept",
            command=self.accept_request
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Schedule Session",
            command=self.schedule_session
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Reject",
            command=self.reject_request
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

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "Request ID",
            "Student",
            "Skill",
            "Availability",
            "Urgency",
            "Status",
            "Requested On"
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

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

        self.tree.column(
            "Request ID",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Student",
            width=200
        )

        self.tree.column(
            "Skill",
            width=200
        )

        self.tree.column(
            "Availability",
            width=220
        )

        self.tree.column(
            "Urgency",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Status",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Requested On",
            width=150,
            anchor="center"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_request_selected
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

        self.selected_request_id = None

        for row in self.tree.get_children():
            self.tree.delete(row)

        requests = student_service.get_incoming_requests(
            self.user["user_id"]
        )

        for request in requests:

            self.tree.insert(
                "",
                "end",
                values=request
            )

    def on_request_selected(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_request_id = values[0]

    def accept_request(self):

        if self.selected_request_id is None:

            messagebox.showwarning(
                "Select Request",
                "Please select a request first."
            )

            return

        success = student_service.approve_request(
            self.selected_request_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Request accepted."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to accept request."
            )

        self.refresh_table()

    def reject_request(self):

        if self.selected_request_id is None:

            messagebox.showwarning(
                "Select Request",
                "Please select a request first."
            )

            return

        success = student_service.reject_request(
            self.selected_request_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Request rejected."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to reject request."
            )

        self.refresh_table()

    def schedule_session(self):

        if self.selected_request_id is None:

            messagebox.showwarning(
                "Select Request",
                "Please select a request first."
            )

            return

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        status = values[5]

        if status != "ACCEPTED":

            messagebox.showwarning(
                "Not Allowed",
                "Only accepted requests can be scheduled."
            )

            return

        dialog = SessionDialog(
            self
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        session_date, meeting_detail = dialog.result

        request_id = values[0]

        offer_id = self.get_offer_id_from_request(
            request_id
        )

        success = student_service.create_session(
            offer_id,
            request_id,
            session_date,
            meeting_detail
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Session scheduled successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to create session."
            )

    def get_offer_id_from_request(self,request_id):

        connection = None
        cursor = None

        try:

            from database.db_connection import db

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT OFFER_ID
                FROM REQUESTS
                WHERE REQUEST_ID = :id
            """, {
                "id": request_id
            })

            row = cursor.fetchone()

            if row:
                return row[0]

            return None

        finally:

            try:
                if cursor:
                    cursor.close()
            except:
                pass

            try:
                if connection:
                    connection.close()
            except:
                pass