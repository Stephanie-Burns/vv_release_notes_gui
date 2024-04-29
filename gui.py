
import os
import webbrowser

from typing import Dict

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Listbox, Scrollbar, Entry, Button

import constants
import email_operations
import serializer
import utils


# ============================================================================


def setup_hotlink_buttons(root: tk) -> None:
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, padx=20, pady=(20, 10), fill=tk.X)

    # Label for the download link
    label = tk.Label(button_frame, text="Helpful Web Addresses:")
    label.pack(side=tk.LEFT, padx=10)

    # Button for the project's Git repository
    git_button = tk.Button(
        button_frame,
        text="Git Repo",
        command=lambda: utils.open_url(constants.GIT_REPO_URL)
    )
    git_button.pack(side=tk.RIGHT, padx=5)

    # Button for the official Viper website
    viper_button = tk.Button(
        button_frame,
        text="Official Patch Notes",
        command=lambda: utils.open_url(constants.OFFICIAL_PATCH_NOTES_URL)
    )
    viper_button.pack(side=tk.RIGHT, padx=5)

    # Button for the Google Drive beta release folder
    gdrive_button = tk.Button(
        button_frame,
        text="Beta Releases",
        command=lambda: utils.open_url(constants.GDRIVE_BETA_FOLDER_URL)
    )
    gdrive_button.pack(side=tk.RIGHT, padx=5)


# ============================================================================


def setup_manage_buttons(root: tk, app_config: Dict) -> None:
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, padx=20, pady=(20, 20), fill=tk.X)

    # Label for the Manage link
    label = tk.Label(button_frame, text="Manage:")
    label.pack(side=tk.LEFT, padx=10)

    # Button for the modifying Email Credentials
    email_credentials_button = tk.Button(
        button_frame,
        text="Email Credentials",
        command=lambda: open_credentials_window(app_config)
    )
    email_credentials_button.pack(side=tk.RIGHT, padx=5)

    # Button modifying the Release Notes file
    release_notes_open_file_button = tk.Button(
        button_frame,
        text="Release Notes",
        command=lambda: open_file_with_default_editor(constants.RELEASE_NOTES_FILE_PATH)
    )
    release_notes_open_file_button.pack(side=tk.RIGHT, padx=5)


def open_credentials_window(app_config: dict):
    # Create a top-level window for credentials input
    credentials_window = tk.Toplevel()
    credentials_window.title("Manage Email Credentials")
    credentials_window.geometry("350x200")

    # Frame for username entry
    username_frame = ttk.Frame(credentials_window)
    username_frame.pack(pady=10, padx=10, fill=tk.X)

    ttk.Label(username_frame, text="Username (Viper Email):").pack(anchor='nw')
    username_entry = ttk.Entry(username_frame)
    username_entry.pack(side=tk.TOP, fill=tk.X, padx=10)

    # Load saved username if available
    saved_username = utils.get_obfuscated_data('google_email_address', app_config)
    if saved_username:
        username_entry.insert(0, saved_username)

    # Frame for password entry
    password_frame = ttk.Frame(credentials_window)
    password_frame.pack(pady=10, padx=10, fill=tk.X)

    ttk.Label(password_frame, text="Password (Google App password):").pack(anchor='nw')
    password_entry = ttk.Entry(password_frame, show='*')
    password_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)

    # Toggle button for showing or hiding the password
    def toggle_password():
        if password_entry.cget('show') == '':
            password_entry.config(show='*')
            show_password_button.config(text="Show")
        else:
            password_entry.config(show='')
            show_password_button.config(text="Hide")

    show_password_button = ttk.Button(password_frame, text="Show", command=toggle_password)
    show_password_button.pack(side=tk.LEFT, padx=(5, 0))

    # Load saved password if available
    saved_password = utils.get_obfuscated_data('google_email_app_password', app_config)
    if saved_password:
        password_entry.insert(0, saved_password)

    # Button to save credentials
    save_button = ttk.Button(
        credentials_window,
        text="Save Credentials",
        command=lambda: save_credentials(credentials_window, username_entry.get(), password_entry.get(), app_config)
    )
    save_button.pack(pady=20)


def save_credentials(password_window: tk.Toplevel, username, password, app_config: Dict) -> None:

    if not email_operations.is_valid_email(username):
        messagebox.showinfo("Value Error", "Please supply a valid email address.", parent=password_window)
        return

    obf_username = utils.obfuscator(username, constants.GIT_REPO_URL)
    obf_username = utils.encode_to_base64(obf_username)
    app_config['email_credentials']['google_email_address'] = obf_username

    obf_password = utils.obfuscator(password, constants.GIT_REPO_URL)
    obf_password = utils.encode_to_base64(obf_password)
    app_config['email_credentials']['google_email_app_password'] = obf_password

    print("Credentials saved:", username, password)
    print(f"{app_config['email_credentials']['google_email_address']=}")
    print(f"{app_config['email_credentials']['google_email_app_password']=}")

    toggle_x(app_config)

    password_window.destroy()


def open_file_with_default_editor(file_path: str) -> None:
    try:
        if os.path.exists(file_path):
            file_url = 'file://' + os.path.abspath(file_path)
            webbrowser.open(file_url)
        else:
            messagebox.showinfo("ERROR: Open File", f"File does not exist: {file_path}")
            # TODO: Log error
    except Exception as e:
        messagebox.showinfo("ERROR: Open File", f"Failed to open file {e}")
        # TODO: Log exception


# ============================================================================


def setup_build_html_field(root: tk, app_config: Dict) -> None:
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.X)

    # grab value if already saved in config
    if isinstance(app_config['configuration_history'].get('build_html'), tk.BooleanVar):
        build_html_var = app_config['configuration_history'].get('build_html')
    else:
        build_html_var = tk.BooleanVar(value=False)

    build_html_checkbox = tk.Checkbutton(frame, text=" Build HTML", variable=build_html_var)
    build_html_checkbox.pack(side=tk.LEFT, padx=10, fill=tk.X)

    app_config['configuration_history']['build_html'] = build_html_var


# ============================================================================


def setup_git_push_field(root: tk, app_config: Dict) -> None:
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.X)

    # grab value if already saved in config
    if isinstance(app_config['configuration_history'].get('push_to_github'), tk.BooleanVar):
        push_github_var = app_config['configuration_history'].get('push_to_github')
    else:
        push_github_var = tk.BooleanVar(value=False)

    push_github_checkbox = tk.Checkbutton(frame, text=" Push to GitHub", variable=push_github_var)
    push_github_checkbox.pack(side=tk.LEFT, padx=10, pady=(0, 0), fill=tk.X)

    app_config['configuration_history']['push_to_github'] = push_github_var


# ============================================================================


def setup_email_manager_frame(root: tk, display_text: str, key: str, app_config: Dict) -> None:
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.X)

    # grab value if already saved in config
    if isinstance(app_config['configuration_history'].get(key), tk.BooleanVar):
        check_var = app_config['configuration_history'].get(key)
    else:
        check_var = tk.BooleanVar(value=False)

    # Checked State Button
    check_button = tk.Checkbutton(frame, text=display_text, variable=check_var, state=tk.DISABLED)
    check_button.pack(side=tk.LEFT, padx=10)

    # Manage Button
    if app_config['state_managers'].get(key):
        manage_button = app_config['state_managers'].get(key)

    else:
        manage_button = tk.Button(
            frame,
            text="Manage Recipients",
            command=lambda: open_email_manager(root, key, app_config)
        )
    manage_button.pack(side=tk.RIGHT, padx=10)

    # State
    app_config['configuration_history'][key] = check_var
    app_config['state_managers'][key] = check_button
    toggle_x(app_config)


def setup_email_window(email_window: Toplevel, email_list: Listbox, key: str, app_config: Dict) -> None:
    entry_frame = tk.Frame(email_window)
    entry_frame.pack(padx=10, pady=10, fill=tk.X)

    email_entry = Entry(entry_frame, width=50)
    email_entry.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)

    add_button = Button(
        entry_frame,
        text="Add Email",
        command=lambda: _add_email_and_toggle(email_window, email_entry, email_list, key, app_config)
    )
    add_button.pack(side=tk.LEFT, padx=10)

    list_frame = tk.Frame(email_window)
    list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    email_list = Listbox(list_frame, height=10, width=50)

    key = 'html_file_recipients' if key == 'email_html_file' else 'release_announcement_recipients'
    emails = utils.get_config_value(key, app_config['email_distribution_lists'])

    if emails:
        for email in emails:
            email_list.insert(tk.END, email)

    email_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(list_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the listbox to scroll with the scrollbar
    email_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=email_list.yview)

    email_list.config(yscrollcommand=scrollbar.set)
    remove_button = Button(
        email_window,
        text="Remove Selected",
        command=lambda: _remove_email_and_toggle(email_window, email_list, key, app_config)
    )
    remove_button.pack(pady=10)


def open_email_manager(root: tk, key: str, app_config: Dict) -> None:
    title = 'Html File Recipients' if key == 'email_html_file' else 'Release Announcement Recipients'
    email_window = Toplevel(root)
    email_window.title(f"Manage {title}")
    email_list = Listbox(email_window, height=10, width=50)
    setup_email_window(email_window, email_list, key, app_config)
    email_operations.load_emails_from_config(root, email_list, key, app_config)


def _add_email_and_toggle(email_window, email_entry, email_list, key, app_config):
    email_operations.add_email(email_window, email_entry, email_list, key, app_config)
    toggle_x(app_config)


def _remove_email_and_toggle(email_window, email_list, key, app_config):
    email_operations.remove_email(email_window, email_list, key, app_config)
    toggle_x(app_config)


# ============================================================================


def setup_download_link_field(root: tk, app_config: Dict) -> None:
    # Frame for the download link
    download_frame = tk.Frame(root)
    download_frame.pack(pady=(20, 5), padx=20, fill=tk.X)

    # Label for the download link
    label = tk.Label(download_frame, text="ViperVision Download Link:")
    label.pack(side=tk.LEFT, padx=10)

    # Entry widget for the download link
    if utils.get_config_value('vipervision_download_link', app_config['configuration_history']):
        download_link_var = app_config['configuration_history']['vipervision_download_link']
    else:
        download_link_var = tk.StringVar()

    download_entry = tk.Entry(download_frame, width=50, textvariable=download_link_var)
    download_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

    download_link_var.trace_add('write', lambda name, index, mode: toggle_x(app_config))
    app_config['configuration_history']['vipervision_download_link'] = download_link_var


# ============================================================================


def setup_run_button(root: tk, app_config: Dict):
    run_button_frame = tk.Frame(root)
    run_button_frame.pack(padx=10, pady=20)

    run_button = ttk.Button(
        run_button_frame,
        text="Run",
        command=lambda: run_operations(app_config),
        width=20
    )
    run_button.pack(side=tk.LEFT, padx=5)


def run_operations(app_config: Dict) -> None:
    # Placeholder for operations to be run
    x = app_config.get('configuration_history')
    y = app_config.get('email_distribution_lists')
    z = app_config.get('email_credentials')

    print("Running operations...")
    print(app_config)
    print(f"{utils.get_config_value('build_html', x)=}")
    print(f"{utils.get_config_value('push_to_github', x)=}")
    print(f"{utils.get_config_value('email_html_file', x)=}")
    print(f"{utils.get_config_value('email_release_announcement', x)=}")
    print(f"{utils.get_config_value('vipervision_download_link', x)=}")

    print(f"{utils.get_config_value('release_announcement_recipients', y)=}")
    print(f"{utils.get_config_value('html_file_recipients', y)=}")

    print(f"{utils.get_config_value('google_email_address', z)=}")
    print(f"{utils.get_config_value('google_email_app_password', z)=}")

    serializer.save_configuration_to_file(app_config)


# ============================================================================

def toggle_x(app_config: Dict):
    """Sorry for the mess!"""
    html_state = app_config['state_managers'].get('email_html_file')
    email_state = app_config['state_managers'].get('email_release_announcement')

    if (
            utils.get_config_value('google_email_address', app_config['email_credentials'])
            and utils.get_config_value('google_email_app_password', app_config['email_credentials'])
            and utils.get_config_value('vipervision_download_link', app_config['configuration_history'])
    ):
        if html_state:
            if utils.get_config_value('html_file_recipients', app_config['email_distribution_lists']):
                app_config['state_managers']['email_html_file'].config(state=tk.NORMAL)
            else:
                app_config['configuration_history']['email_html_file'] = tk.BooleanVar(value=False)
                app_config['state_managers']['email_html_file'].config(
                    state=tk.DISABLED, variable=app_config['configuration_history']['email_html_file']
                )

        if email_state:
            if utils.get_config_value('release_announcement_recipients', app_config['email_distribution_lists']):
                app_config['state_managers']['email_release_announcement'].config(state=tk.NORMAL)
            else:
                app_config['configuration_history']['email_release_announcement'] = tk.BooleanVar(value=False)
                app_config['state_managers']['email_release_announcement'].config(
                    state=tk.DISABLED, variable=app_config['configuration_history']['email_release_announcement']
                )

    else:
        if html_state:
            app_config['configuration_history']['email_html_file'] = tk.BooleanVar(value=False)
            app_config['state_managers']['email_html_file'].config(
                state=tk.DISABLED, variable=app_config['configuration_history']['email_html_file']
            )

        if email_state:
            app_config['configuration_history']['email_release_announcement'] = tk.BooleanVar(value=False)
            app_config['state_managers']['email_release_announcement'].config(
                state=tk.DISABLED, variable=app_config['configuration_history']['email_release_announcement']
            )
