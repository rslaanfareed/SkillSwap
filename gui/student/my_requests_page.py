import customtkinter as ctk
from tkinter import ttk, messagebox

from services.student_service import student_service


class MyRequestsPage(ctk.CTkFrame):

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
            text="My Requests",
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
            text="Cancel Request",
            command=self.cancel_request
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
            "Skill",
            "Offered By",
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
            "Skill",
            width=200
        )

        self.tree.column(
            "Offered By",
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

        requests = student_service.get_my_requests(
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

    def cancel_request(self):

        if self.selected_request_id is None:

            messagebox.showwarning(
                "Select Request",
                "Please select a request first."
            )

            return

        selected = self.tree.selection()

        values = self.tree.item(
            selected[0]
        )["values"]

        status = values[5]

        if status != "PENDING":

            messagebox.showwarning(
                "Not Allowed",
                "Only pending requests can be cancelled."
            )

            return

        confirm = messagebox.askyesno(
            "Cancel Request",
            "Are you sure you want to cancel this request?"
        )

        if not confirm:
            return

        success = student_service.cancel_request(
            self.selected_request_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Request cancelled successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to cancel request."
            )

        self.refresh_table()