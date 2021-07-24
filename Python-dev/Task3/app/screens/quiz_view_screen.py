import tkinter as tk

from app.util import util_data
from app.widgets.vertical_scrolled_frame import VerticalScrolledFrame


class QuizViewScreen:
    def __init__(self, master, quiz):
        self.master = master
        self.quiz = quiz
        self.replies = {}
        self.questions = []
        self.frame = tk.Frame(self.master)
        self.questions_frame = VerticalScrolledFrame(self.frame)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        subject_label = tk.Label(
            self.frame,
            text=util_data.quiz_db.subjects()[self.quiz.subject_code - 1].name,
            font=("Arial", 25),
        )
        subject_label.pack(pady=5)
        self.questions_frame.pack()

        btn_frame = tk.Frame(self.frame)
        if util_data.is_teacher:
            btn_add_question = tk.Button(
                btn_frame,
                text="Add Question",
                font=("Arial", 13),
                command=self.add_question,
            )
            btn_add_question.pack(side=tk.LEFT, padx=10, pady=10)
        btn_done = tk.Button(
            btn_frame, text="Done", font=("Arial", 13), command=self.go_back
        )
        btn_done.pack(side=tk.LEFT, padx=10)
        btn_frame.pack()
        self.refresh()

    def refresh(self):
        questions = util_data.quiz_db.questions_of_quiz(self.quiz)
        q_ids = [q.id for q in questions]
        r_ids = [q.question.id for q in self.questions]
        for i in range(len(q_ids)):
            if q_ids[i] not in r_ids:
                t = _QuestionItem(
                    self.frame,
                    self.questions_frame.interior,
                    questions[i],
                    i,
                    self.quiz,
                    self.record_chosen,
                )
                self.questions.append(t)

    def add_question(self, *args):
        top_level = tk.Toplevel(self.master)
        questions = util_data.quiz_db.questions_of_quiz(self.quiz)

        from .question_screen import QuestionScreen

        QuestionScreen(
            top_level,
            None,
            len(questions),
            self.quiz,
            self.refresh,
            None,
        )

    def go_back(self, *args):
        if not util_data.is_teacher:
            for q, r in self.replies.items():
                if q.correct_answer_idx == r:
                    util_data.student_score.score += util_data.correct_respond
                else:
                    util_data.student_score.score += util_data.wrong_respond
            util_data.score_db.update_score(util_data.student_score)
            from .score_display_screen import ScoreDisplayScreen

            ScoreDisplayScreen(self.master)
            self.frame.destroy()
            return

        from .quiz_list_screen import QuizListScreen

        QuizListScreen(self.master)
        self.frame.destroy()

    def record_chosen(self, question, option_idx):
        self.replies[question] = option_idx
        for q in self.questions:
            if q.question.id == question.id:
                q.mark_responded()


class _QuestionItem:
    def __init__(self, master, frame, question, idx, quiz, record_chosen):
        self.master = master
        self.quiz = quiz
        self.question = question
        self.record_chosen = record_chosen
        self.idx = idx
        self.frame = tk.Frame(frame, highlightbackground="black", highlightthickness=1)
        self.question_num_label = tk.Label(
            self.frame, text=f"Question {self.idx + 1}", font=("Arial", 16), width=25
        )
        self.load_components()
        self.frame.pack(pady=3, padx=4)

    def load_components(self):
        self.question_num_label.pack()

        from app.util import bind_widgets_in_tag

        bind_widgets_in_tag(
            f"question{self.question.id}", self.frame, self.question_num_label
        )
        self.frame.bind_class(
            f"question{self.question.id}", "<Button>", self.show_question
        )

    def show_question(self, *args):
        from .question_screen import QuestionScreen

        top_level = tk.Toplevel(self.master)

        def on_option_chosen(option):
            self.record_chosen(self.question, option)

        QuestionScreen(
            top_level, self.question, self.idx, self.quiz, None, on_option_chosen
        )

    def mark_responded(self):
        self.question_num_label.configure(bg="green")
