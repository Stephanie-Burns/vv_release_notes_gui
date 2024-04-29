
import tkinter as tk
from tkinter import messagebox
import gui

import serializer


# TODO: block extra windows from spawning when an element which loads a frame is clicked


def on_app_close(root, app_config):
    """Function to handle app closure: saves configuration and cleans up before closing."""
    serializer.save_configuration_to_file(app_config)
    root.after(2000, root.destroy)  # auto-close in milliseconds
    try:
        messagebox.showinfo(
            "Application Closing",
            "Configuration has been saved successfully. \n\nThe app will close shortly."
        )
    except tk.TclError:
        # Prevents log from complaining about popups which aren't closed.
        pass


def main():
    root = tk.Tk()
    root.title("Release Notes Manager")

    app_config = serializer.load_configuration_from_file()
    app_config['state_managers'] = {}

    gui.setup_hotlink_buttons(root)
    gui.setup_manage_buttons(root, app_config)
    gui.setup_build_html_field(root, app_config)
    gui.setup_git_push_field(root, app_config)
    gui.setup_email_manager_frame(
        root, "Email HTML File", "email_html_file", app_config
    )
    gui.setup_email_manager_frame(
        root, "Email Release Announcement", "email_release_announcement", app_config
    )
    gui.setup_download_link_field(root, app_config)
    gui.setup_run_button(root, app_config)

    root.protocol("WM_DELETE_WINDOW", lambda: on_app_close(root, app_config))
    root.mainloop()


if __name__ == "__main__":
    main()
