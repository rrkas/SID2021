import tkinter as tk

from app.util import util_data


# Home Screen (Student/ Teacher)
class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=20, pady=20)

    # load widgets on screen
    def load_components(self):
        name_frame = tk.Frame(
            self.frame, highlightbackground="black", highlightthickness=1
        )
        name_label = tk.Label(
            name_frame, text=util_data.app_name.upper(), font=("Arial", 30)
        )
        name_label.pack(padx=5, pady=5)
        name_frame.pack(padx=5, pady=5)

        student_btn = tk.Button(
            self.frame,
            text="STUDENT",
            font=("Arial", 15),
            command=lambda: self.start_login(False),
        )
        student_btn.pack(side=tk.LEFT, padx=5, pady=5)

        teacher_btn = tk.Button(
            self.frame,
            text="TEACHER",
            font=("Arial", 15),
            command=lambda: self.start_login(True),
        )
        teacher_btn.pack(side=tk.LEFT, padx=5, pady=5)

    # show login screen
    def start_login(self, is_teacher):
        # update global is_teacher
        util_data.is_teacher = is_teacher

        from .login_screen import LoginScreen

        LoginScreen(tk.Toplevel(self.master), self)

    # start session for logged user
    def start_session(self):
        self.frame.destroy()
        if util_data.is_teacher:
            from .teacher_screen import TeacherScreen

            TeacherScreen(self.master)
        else:
            from .quiz_list_screen import QuizListScreen

            QuizListScreen(self.master)
