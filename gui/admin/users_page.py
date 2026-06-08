import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog

from services.admin_service import admin_service


class UsersPage(ctk.CTkFrame):

    def __init__(self, master, current_user):
        super().__init__(master)

        self.current_user = current_user

        self.selected_user_id = None
        self.tree = None

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
            text="User Management",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        ).pack(pady=20)

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
            text="Activate",
            command=self.activate_selected_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Deactivate",
            command=self.deactivate_selected_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Reset Password",
            command=self.reset_selected_user_password
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.refresh_table
        ).pack(side="left", padx=5)

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "ID",
            "Name",
            "Email",
            "Role",
            "Status",
            "Batch"
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

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Batch", text="Batch")

        self.tree.column(
            "ID",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "Name",
            width=220
        )

        self.tree.column(
            "Email",
            width=280
        )

        self.tree.column(
            "Role",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Status",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Batch",
            width=100,
            anchor="center"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_user_selected
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

        if self.tree is None:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        users = admin_service.get_all_users()

        for user in users:

            self.tree.insert(
                "",
                "end",
                values=user
            )

    def on_user_selected(self, event):

        if self.tree is None:
            return

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_user_id = values[0]

    def activate_selected_user(self):

        if self.selected_user_id is None:

            messagebox.showwarning(
                "Select User",
                "Please select a user first."
            )

            return

        admin_service.activate_user(
            self.selected_user_id
        )

        messagebox.showinfo(
            "Success",
            "User activated."
        )

        self.refresh_table()

    def deactivate_selected_user(self):

        if self.selected_user_id is None:

            messagebox.showwarning(
                "Select User",
                "Please select a user first."
            )

            return

        if self.selected_user_id == self.current_user["user_id"]:

            messagebox.showwarning(
                "Not Allowed",
                "You cannot deactivate yourself."
            )

            return

        admin_service.deactivate_user(
            self.selected_user_id
        )

        messagebox.showinfo(
            "Success",
            "User deactivated."
        )

        self.refresh_table()

    def reset_selected_user_password(self):

        if self.selected_user_id is None:

            messagebox.showwarning(
                "Select User",
                "Please select a user first."
            )

            return

        new_password = simpledialog.askstring(
            "Reset Password",
            "Enter new password:",
            show="*"
        )

        if not new_password:
            return

        admin_service.reset_password(
            self.selected_user_id,
            new_password
        )

        messagebox.showinfo(
            "Success",
            "Password updated successfully."
        )