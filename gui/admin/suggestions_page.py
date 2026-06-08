import customtkinter as ctk
from tkinter import ttk, messagebox

from services.admin_service import admin_service


class SuggestionsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.selected_suggestion_id = None
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

        title = ctk.CTkLabel(
            self,
            text="Skill Suggestions",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        title.pack(pady=20)

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
            text="Approve",
            command=self.approve_suggestion
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Reject",
            command=self.reject_suggestion
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
            "Suggestion ID",
            "User ID",
            "Skill Name",
            "Category",
            "Status"
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
            "Suggestion ID",
            text="Suggestion ID"
        )

        self.tree.heading(
            "User ID",
            text="User ID"
        )

        self.tree.heading(
            "Skill Name",
            text="Skill Name"
        )

        self.tree.heading(
            "Category",
            text="Category"
        )

        self.tree.heading(
            "Status",
            text="Status"
        )

        self.tree.column(
            "Suggestion ID",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "User ID",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Skill Name",
            width=280
        )

        self.tree.column(
            "Category",
            width=220
        )

        self.tree.column(
            "Status",
            width=120,
            anchor="center"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_suggestion_selected
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

        suggestions = admin_service.get_all_suggestions()

        for suggestion in suggestions:

            self.tree.insert(
                "",
                "end",
                values=suggestion
            )

    def on_suggestion_selected(self, event):

        if self.tree is None:
            return

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_suggestion_id = values[0]

    def approve_suggestion(self):

        if self.selected_suggestion_id is None:

            messagebox.showwarning(
                "Select Suggestion",
                "Please select a suggestion first."
            )

            return

        success = admin_service.approve_suggestion(
            self.selected_suggestion_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Suggestion approved."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to approve suggestion."
            )

        self.refresh_table()

    def reject_suggestion(self):

        if self.selected_suggestion_id is None:

            messagebox.showwarning(
                "Select Suggestion",
                "Please select a suggestion first."
            )

            return

        success = admin_service.reject_suggestion(
            self.selected_suggestion_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Suggestion rejected."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to reject suggestion."
            )

        self.refresh_table()