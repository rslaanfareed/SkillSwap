import customtkinter as ctk
from tkinter import ttk, messagebox

from services.student_service import student_service
from gui.student.request_dialog import RequestDialog

class BrowseSkillsPage(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.tree = None
        self.selected_offer_id = None

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
            text="Browse Skills",
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
            text="Request Skill",
            command=self.request_skill
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
            "Offer ID",
            "Student",
            "Skill",
            "Level",
            "Mode",
            "Rating",
            "Reviews"
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
            "Offer ID",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Student",
            width=250
        )

        self.tree.column(
            "Skill",
            width=250
        )

        self.tree.column(
            "Level",
            width=180,
            anchor="center"
        )

        self.tree.column(
            "Mode",
            width=180,
            anchor="center"
        )

        self.tree.column(
            "Rating",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Reviews",
            width=100,
            anchor="center"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_offer_selected
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

        self.selected_offer_id = None

        for row in self.tree.get_children():
            self.tree.delete(row)

        offers = student_service.get_available_offers(
            self.user["user_id"]
        )

        for offer in offers:

            self.tree.insert(
                "",
                "end",
                values=offer
            )

    def on_offer_selected(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.selected_offer_id = values[0]
        self.selected_skill_name = values[2]

    def request_skill(self):

        if self.selected_offer_id is None:

            messagebox.showwarning(
                "Select Offer",
                "Please select an offer first."
            )

            return

        availability_list = (
            student_service.get_offer_availability(
                self.selected_offer_id
            )
        )

        if not availability_list:

            messagebox.showwarning(
                "No Availability",
                "This offer has no availability slots."
            )

            return

        dialog = RequestDialog(
            self,
            availability_list
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        availability_id, urgency, note = dialog.result

        selected = self.tree.selection()

        values = self.tree.item(
            selected[0]
        )["values"]

        offer_id = values[0]
        skill_name = values[2]

        skills = student_service.get_skills()

        skill_id = None

        for skill in skills:

            if skill[1] == skill_name:

                skill_id = skill[0]
                break

        if skill_id is None:

            messagebox.showerror(
                "Error",
                "Skill not found."
            )

            return

        success = student_service.create_request(
            self.user["user_id"],
            offer_id,
            skill_id,
            availability_id,
            urgency,
            note
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Request submitted successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to create request."
            )