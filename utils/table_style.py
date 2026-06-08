from tkinter import ttk


def apply_table_style():

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b",
        rowheight=35,
        borderwidth=0,
        font=("Segoe UI", 11)
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#1f6aa5")
        ]
    )

    style.configure(
        "Treeview.Heading",
        background="#202020",
        foreground="white",
        font=("Segoe UI", 11, "bold"),
        borderwidth=0
    )

    style.map(
        "Treeview.Heading",
        background=[
            ("active", "#2f2f2f")
        ]
    )