import customtkinter as ctk
from tkinter import ttk, messagebox
from gui.student.availability_dialog import AvailabilityDialog
from services.student_service import student_service
from gui.student.offer_dialog import OfferDialog
from gui.student.view_availability_dialog import ViewAvailabilityDialog

class OffersPage(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.tree = None

        self.selected_offer_id = None
        self.selected_skill_id = None
        self.selected_skill_name = None
        self.selected_level = None
        self.selected_mode = None

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
            text="My Offers",
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
            text="Add Offer",
            command=self.add_offer
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Edit Offer",
            command=self.edit_offer
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Delete Offer",
            command=self.delete_offer
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            button_frame,
            text="Add Availability",
            command=self.add_availability
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            button_frame,
            text="View Availability",
            command=self.view_availability
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
            "Skill ID",
            "Skill",
            "Level",
            "Mode"
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
            "Offer ID",
            text="Offer ID"
        )

        self.tree.heading(
            "Skill ID",
            text="Skill ID"
        )

        self.tree.heading(
            "Skill",
            text="Skill"
        )

        self.tree.heading(
            "Level",
            text="Level"
        )

        self.tree.heading(
            "Mode",
            text="Mode"
        )

        self.tree.column(
            "Offer ID",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "Skill ID",
            width=90,
            anchor="center"
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

        for row in self.tree.get_children():
            self.tree.delete(row)

        offers = student_service.get_my_offers(
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
        self.selected_skill_id = values[1]
        self.selected_skill_name = values[2]
        self.selected_level = values[3]
        self.selected_mode = values[4]

    def add_offer(self):

        skills = student_service.get_skills()

        dialog = OfferDialog(
            self,
            skills
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        skill_id, level, mode = dialog.result

        success = student_service.add_offer(
            self.user["user_id"],
            skill_id,
            level,
            mode
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Offer added successfully."
            )

            self.refresh_table()

        else:

            messagebox.showerror(
                "Error",
                "Failed to add offer."
            )

    def edit_offer(self):

        if self.selected_offer_id is None:

            messagebox.showwarning(
                "Select Offer",
                "Please select an offer first."
            )

            return

        skills = student_service.get_skills()

        dialog = OfferDialog(
            self,
            skills,
            {
                "skill_name": self.selected_skill_name,
                "level": self.selected_level,
                "mode": self.selected_mode
            }
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        skill_id, level, mode = dialog.result

        success = student_service.update_offer(
            self.selected_offer_id,
            skill_id,
            level,
            mode
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Offer updated successfully."
            )

            self.refresh_table()

        else:

            messagebox.showerror(
                "Error",
                "Failed to update offer."
            )

    def delete_offer(self):

        if self.selected_offer_id is None:

            messagebox.showwarning(
                "Select Offer",
                "Please select an offer first."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Offer",
            "Are you sure you want to delete this offer?"
        )

        if not confirm:
            return

        success = student_service.delete_offer(
            self.selected_offer_id
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Offer deleted successfully."
            )

            self.refresh_table()

        else:

            messagebox.showerror(
                "Error",
                "Failed to delete offer."
            )

    def add_availability(self):

        if self.selected_offer_id is None:

            messagebox.showwarning(
                "Select Offer",
                "Please select an offer first."
            )

            return

        dialog = AvailabilityDialog(
            self
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        day, slot = dialog.result

        success = (
            student_service.add_availability(
                self.selected_offer_id,
                day,
                slot
            )
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Availability added."
            )

        else:

            messagebox.showerror(
                "Error",
                "Failed to add availability."
            )

    def view_availability(self):

        if self.selected_offer_id is None:

            messagebox.showwarning(
                "Select Offer",
                "Please select an offer first."
            )

            return

        availability = (
            student_service.get_availability_for_offer(
                self.selected_offer_id
            )
        )

        dialog = ViewAvailabilityDialog(
            self,
            availability
        )

        self.wait_window(dialog)