import customtkinter as ctk
from tkinter import messagebox

from services.student_service import student_service


class SuggestSkillDialog(ctk.CTkToplevel):

    def __init__(self, parent, user):

        super().__init__(parent)

        self.user = user

        self.title("Suggest New Skill")
        self.geometry("450x300")

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Suggest New Skill",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=20
        )

        self.skill_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter skill name"
        )

        self.skill_entry.pack(
            fill="x",
            padx=20,
            pady=10
        )

        categories = (
            student_service.get_categories()
        )

        self.category_map = {}

        category_names = []

        for category in categories:

            self.category_map[
                category[1]
            ] = category[0]

            category_names.append(
                category[1]
            )

        self.category_menu = ctk.CTkOptionMenu(
            self,
            values=category_names
        )

        self.category_menu.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Submit Suggestion",
            command=self.submit
        ).pack(
            pady=20
        )

    def submit(self):

        skill_name = (
            self.skill_entry.get().strip()
        )

        if not skill_name:

            messagebox.showwarning(
                "Missing Skill",
                "Please enter a skill name."
            )

            return

        category_name = (
            self.category_menu.get()
        )

        category_id = (
            self.category_map[
                category_name
            ]
        )

        success = (
            student_service.submit_skill_suggestion(
                self.user["user_id"],
                skill_name,
                category_id
            )
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Suggestion submitted."
            )

            self.destroy()

        else:

            messagebox.showwarning(
                "Already Exists",
                "This skill already exists."
            )