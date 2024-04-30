
import tkinter as tk

import gui
import logger_config
import serializer


# TODO: block extra windows from spawning when an element which loads a frame is clicked
# TODO: edit button for web addresses
# TODO: stop saving download address


def on_app_close(root, app_config):
    """Function to handle app closure: saves configuration and cleans up before closing."""
    serializer.save_configuration_to_file(app_config)
    gui.kill(root)


def main():
    root = tk.Tk()
    root.title("Release Notes Manager")

    # Logging setup
    log_widget = gui.get_logging_widget(root)
    logger = logger_config.setup_logging(log_widget)
    logger.info("=" * 74)
    logger.info("Logging started...")

    # Config Setup
    app_config = serializer.load_configuration_from_file()
    app_config['state_managers'] = {}

    # Gui Setup
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
    log_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: on_app_close(root, app_config))
    root.mainloop()


if __name__ == "__main__":
    main()
