import tkinter as tk

from app.util import util_data


class ScoreDisplayScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        msg_label = tk.Label(self.frame, text="Your score has been recorded!")
        msg_label.pack()
        name_label = tk.Label(
            self.frame,
            text="Name:\n" + util_data.student_score.name,
            font=("Arial", 17),
        )
        name_label.pack(pady=5)
        regd_num_label = tk.Label(
            self.frame,
            text="Registration Number:\n" + util_data.student_score.regd_num,
            font=("Arial", 17),
        )
        regd_num_label.pack(pady=5)
        score_label = tk.Label(
            self.frame,
            text="Score:\n" + str(util_data.student_score.score),
            font=("Arial", 17),
        )
        score_label.pack(pady=5)

        btn_frame = tk.Frame(self.frame)

        def exit_app(*args):
            self.master.destroy()

        btn_exit = tk.Button(
            btn_frame, text="EXIT", command=exit_app, font=("Arial", 14)
        )
        btn_exit.pack(side=tk.LEFT)

        def restart(*args):
            from .quiz_list_screen import QuizListScreen

            QuizListScreen(self.master)
            self.frame.destroy()

        btn_restart = tk.Button(
            btn_frame, text="RESTART", command=restart, font=("Arial", 14)
        )
        btn_restart.pack(side=tk.LEFT, padx=5)

        btn_frame.pack(pady=5)
