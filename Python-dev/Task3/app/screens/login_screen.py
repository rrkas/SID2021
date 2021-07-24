import tkinter as tk
from tkinter import messagebox

from app.util import util_data


# Login Screen (Student/ Teacher)
class LoginScreen:
    def __init__(self, master, home_obj):
        self.master = master
        self.master.grab_set()  # to make home screen disabled
        self.home_obj = home_obj
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=20, pady=20)

    # load the widgets on the screen
    def load_components(self):
        name_frame = tk.Frame(
            self.frame, highlightbackground="black", highlightthickness=1
        )
        name_label = tk.Label(
            name_frame, text=util_data.app_name.upper(), font=("Arial", 30)
        )
        name_label.pack(padx=5, pady=5)
        name_frame.pack(padx=5, pady=5)

        username_frame = tk.Frame(
            self.frame, highlightbackground="black", highlightthickness=1
        )
        username_var = tk.StringVar()
        username_label = tk.Label(
            username_frame,
            text="USERNAME: " if util_data.is_teacher else "Enter name: ",
        )
        username_label.pack(side=tk.LEFT)
        username_entry = tk.Entry(username_frame, textvariable=username_var)
        username_entry.pack(side=tk.LEFT, padx=5, pady=10)
        username_frame.pack(pady=10)

        # 2nd field
        # password              : teacher
        # registration number   : student
        field2_var = tk.StringVar()
        field2_frame = tk.Frame(
            self.frame, highlightbackground="black", highlightthickness=1
        )
        field2_label = tk.Label(
            field2_frame,
            text="PASSWORD: " if util_data.is_teacher else "Enter Registration No: ",
        )
        field2_label.pack(side=tk.LEFT)
        field2_entry = tk.Entry(field2_frame, textvariable=field2_var)
        field2_entry.pack(side=tk.LEFT, padx=5, pady=10)
        field2_frame.pack(pady=10)

        # check credentials and log in
        def login_user():
            # if in debug mode, bypass the auth check
            if util_data.debug:
                # inflate demo data if not filled
                util_data.student_score.name = (
                    username_var.get()
                    if len(username_var.get()) > 0
                    else "Student Demo"
                )
                util_data.student_score.regd_num = (
                    field2_var.get() if len(field2_var.get()) > 0 else "Regd Demo"
                )
                self.start_session()
                return
            if util_data.is_teacher:
                if username_var.get() == "teacher123" and field2_var.get() == "pass123":
                    self.start_session()
                else:
                    messagebox.showerror(
                        "Invalid Credentials", "Username and password mismatch!"
                    )
            else:
                # update student data for current session
                util_data.student_score.name = username_var.get()
                util_data.student_score.regd_num = field2_var.get()
                self.start_session()

        login_btn = tk.Button(
            self.frame,
            text="LOGIN!" if util_data.is_teacher else "START!",
            command=login_user,
        )
        login_btn.pack(pady=10)

    # start session for the student/ teacher
    def start_session(self):
        self.home_obj.start_session()
        self.master.destroy()
