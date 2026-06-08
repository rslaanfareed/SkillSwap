import customtkinter as ctk
from tkinter import ttk, messagebox

from gui.components.skill_dialog import SkillDialog
from services.admin_service import admin_service


class SkillsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.selected_skill_id = None
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
            text="Skills Management",
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
            text="Add Skill",
            command=self.add_skill
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Delete Skill",
            command=self.delete_skill
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
            "ID",
            "Skill Name",
            "Category"
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
            "ID",
            text="ID"
        )

        self.tree.heading(
            "Skill Name",
            text="Skill Name"
        )

        self.tree.heading(
            "Category",
            text="Category"
        )

        self.tree.column(
            "ID",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "Skill Name",
            width=350
        )

        self.tree.column(
            "Category",
            width=250
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_skill_selected
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

        skills = admin_service.get_all_skills()

        for skill in skills:

            self.tree.insert(
                "",
                "end",
                values=skill
            )

    def on_skill_selected(self, event):

        if self.tree is None:
            return

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_skill_id = values[0]

    def add_skill(self):

        categories = admin_service.get_skill_categories()

        dialog = SkillDialog(
            self,
            categories
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        skill_name, category_id = dialog.result

        success = admin_service.add_skill(
            skill_name,
            category_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Skill added successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to add skill."
            )

        self.refresh_table()

    def delete_skill(self):

        if self.selected_skill_id is None:

            messagebox.showwarning(
                "Select Skill",
                "Please select a skill first."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Skill",
            "Are you sure?"
        )

        if not confirm:
            return

        success = admin_service.delete_skill(
            self.selected_skill_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Skill deleted successfully."
            )

        else:

            messagebox.showerror(
                "Cannot Delete",
                "Skill is being used elsewhere."
            )

        self.refresh_table()