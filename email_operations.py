
import tkinter as tk
import re
from tkinter import messagebox
from typing import Dict


def add_email(parent_frame: tk, entry_widget: tk, list_widget: tk.Listbox, key: str, app_config: Dict) -> None:

    email = entry_widget.get()

    if not is_valid_email(email):
        messagebox.showinfo("Value Error", "Please supply a valid email address.", parent=parent_frame)
        return

    if email not in list_widget.get(0, tk.END):

        list_widget.insert(tk.END, email)
        entry_widget.delete(0, tk.END)
        app_config['email_distribution_lists'][key] = [list_widget.get(i) for i in range(list_widget.size())]
        return

    messagebox.showinfo("Duplicate Error", "This email is already added.", parent=parent_frame)


def remove_email(parent_frame: tk, list_widget: tk.Listbox, key: str, app_config: Dict) -> None:

    try:

        selected_index = list_widget.curselection()[0]
        list_widget.delete(selected_index)
        app_config['email_distribution_lists'][key] = [list_widget.get(i) for i in range(list_widget.size())]

    except IndexError:

        messagebox.showinfo("Selection Error", "Please select an email to remove.", parent=parent_frame)


def load_emails_from_config(parent_frame: tk, list_widget: tk.Listbox, key: str, app_config: Dict) -> None:

    print(key)
    key = 'release_announcement_recipients' if key == 'email_release_announcement' else 'html_file_recipients'

    try:

        all_emails = app_config['email_distribution_lists']
        list_widget.delete(0, tk.END)

        for email in all_emails.get(key, []):
            list_widget.insert(tk.END, email)

    except Exception as e:

        messagebox.showerror("Error", f"Failed to load emails: {str(e)}", parent=parent_frame)


def is_valid_email(email: str) -> bool:

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False
