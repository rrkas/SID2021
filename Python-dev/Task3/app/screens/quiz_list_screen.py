import tkinter as tk

from app.util import util_data
from app.widgets.vertical_scrolled_frame import VerticalScrolledFrame


# Quiz List Screen (Student/ Teacher)
class QuizListScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    # load widgets on screen
    def load_components(self):
        heading_label = tk.Label(self.frame, text="Quizzes", font=("Arial", 25, "bold"))
        heading_label.pack()
        quizzes = util_data.quiz_db.quizzes()
        quizzes_frame = VerticalScrolledFrame(self.frame)
        quizzes_frame.pack()
        for quiz in quizzes:
            _QuizItem(self.master, self.frame, quizzes_frame, quiz)
        if util_data.is_teacher:
            back_btn = tk.Button(self.frame, text="Go Back", command=self.go_back)
            back_btn.pack()

    def go_back(self, *args):
        from .teacher_screen import TeacherScreen

        TeacherScreen(self.master)
        self.frame.destroy()


# row of each quiz
class _QuizItem:
    def __init__(self, master, frame, list_frame, quiz):
        self.root = master
        self.master = frame
        self.list_frame = list_frame
        self.quiz = quiz
        self.frame = tk.Frame(
            list_frame, highlightbackground="black", highlightthickness=1
        )
        self.load_components()
        self.frame.pack(padx=5, pady=5)

    def load_components(self):
        subject = util_data.quiz_db.subject_of_quiz(self.quiz)
        if subject:
            subject_name_label = tk.Label(self.frame, text=subject.name, width=10)
            subject_name_label.pack(side=tk.LEFT, padx=5, anchor="w", pady=5)

            options_count_label = tk.Label(
                self.frame, text=str(self.quiz.num_options) + " options", width=10
            )
            options_count_label.pack(side=tk.LEFT, padx=5, anchor="w")

            question_count_label = tk.Label(
                self.frame,
                text=str(len(util_data.quiz_db.questions_of_quiz(self.quiz)))
                + " questions",
                width=10,
            )
            question_count_label.pack(side=tk.LEFT, padx=5, anchor="w")

            from app.util import bind_widgets_in_tag

            bind_widgets_in_tag(
                f"quiz{self.quiz.id}",
                self.frame,
                subject_name_label,
                options_count_label,
                question_count_label,
            )
            self.frame.bind_class(f"quiz{self.quiz.id}", "<Button>", self.show_quiz)

    def show_quiz(self, *args):
        from .quiz_view_screen import QuizViewScreen

        QuizViewScreen(self.root, self.quiz)
        self.master.destroy()
