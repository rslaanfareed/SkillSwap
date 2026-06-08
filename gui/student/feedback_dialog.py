from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox


class FeedbackDialog(ctk.CTkToplevel):
    def __init__(self, master, on_submit):
        super().__init__(master)
        self.on_submit = on_submit

        self.title('Give Feedback')
        self.geometry('460x390')
        self.resizable(False, False)
        self.transient(master.winfo_toplevel())
        self.grab_set()

        ctk.CTkLabel(
            self,
            text='Give Feedback',
            font=ctk.CTkFont(size=24, weight='bold'),
        ).pack(anchor='w', padx=24, pady=(24, 12))

        ctk.CTkLabel(self, text='Rating (1-5)').pack(anchor='w', padx=24, pady=(4, 6))
        self.rating = ctk.CTkOptionMenu(self, values=['1', '2', '3', '4', '5'])
        self.rating.set('5')
        self.rating.pack(fill='x', padx=24, pady=(0, 14))

        ctk.CTkLabel(self, text='Feedback Text').pack(anchor='w', padx=24, pady=(4, 6))
        self.feedback_text = ctk.CTkTextbox(self, height=150)
        self.feedback_text.pack(fill='both', expand=True, padx=24, pady=(0, 14))

        ctk.CTkButton(self, text='Submit', command=self._submit).pack(fill='x', padx=24, pady=(0, 24))

        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.after(20, self.focus_force)

    def _submit(self):
        try:
            self.on_submit(int(self.rating.get()), self.feedback_text.get('1.0', 'end').strip())
        except Exception as exc:
            messagebox.showerror('Error', str(exc), parent=self)
            return

        self.destroy()
