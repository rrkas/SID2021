import tkinter as tk
import tkinter.ttk as ttk

from app.models.quiz import Quiz
from app.util import util_data
from .quiz_list_screen import QuizListScreen


class TeacherScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        subject_var = tk.StringVar()
        subject_frame = tk.Frame(self.frame)
        subject_label = tk.Label(subject_frame, text="Subject: ")
        subject_label.pack(side=tk.LEFT)
        subject_combobox = ttk.Combobox(
            subject_frame,
            textvariable=subject_var,
        )
        subject_combobox["values"] = tuple(
            map(lambda s: s.name, util_data.quiz_db.subjects())
        )
        subject_combobox.pack(side=tk.RIGHT)
        subject_frame.pack()

        num_options_var = tk.IntVar()
        num_options_frame = tk.Frame(self.frame)
        num_options_label = tk.Label(num_options_frame, text="No of options: ")
        num_options_label.pack(side=tk.LEFT)
        num_options_entry = tk.Entry(num_options_frame, textvariable=num_options_var)
        num_options_entry.pack(side=tk.LEFT)
        num_options_frame.pack(pady=10)

        def show_quiz_list(*args):
            QuizListScreen(self.master)
            self.frame.destroy()

        btn_frame = tk.Frame(self.frame)

        btn_width = 15
        pady = padx = 5

        btn_quiz_list = tk.Button(
            btn_frame, text="All Quizzes", command=show_quiz_list, width=btn_width
        )
        btn_quiz_list.grid(row=0, column=0, padx=padx, pady=pady)

        def add_subject():
            def refresh():
                subject_combobox["values"] = tuple(
                    map(lambda s: s.name, util_data.quiz_db.subjects())
                )

            top_level = tk.Toplevel(self.master)
            from .subject_screen import SubjectScreen

            SubjectScreen(top_level, refresh)

        btn_add_subject = tk.Button(
            btn_frame, text="Add Subject", command=add_subject, width=btn_width
        )
        btn_add_subject.grid(row=0, column=1, padx=padx, pady=pady)

        def make_quiz():
            if subject_combobox.current() > -1:
                quiz = Quiz(
                    subj_code=util_data.quiz_db.subjects()[
                        subject_combobox.current()
                    ].id,
                    num_options=num_options_var.get(),
                )
                util_data.quiz_db.update_quiz(quiz=quiz)
                from .quiz_view_screen import QuizViewScreen

                QuizViewScreen(master=self.master, quiz=quiz)
                self.frame.destroy()

        btn_make_quiz = tk.Button(
            btn_frame, text="Make Quiz", command=make_quiz, width=btn_width
        )
        btn_make_quiz.grid(row=1, column=0, padx=padx, pady=pady)

        def show_scores(*args):
            from .scores_screen import ScoresScreen

            ScoresScreen(self.master)
            self.frame.destroy()

        btn_scores = tk.Button(
            btn_frame, text="All Scores", command=show_scores, width=btn_width
        )
        btn_scores.grid(row=1, column=1, padx=padx, pady=pady)

        btn_frame.pack(pady=10)
