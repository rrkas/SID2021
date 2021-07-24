import tkinter as tk
from tkinter import messagebox

from app.models.question import Question
from app.util import util_data, bind_widgets_in_tag


# Question Screen (Student/ Teacher)
class QuestionScreen:
    def __init__(self, master, question, idx, quiz, refresh, on_option_chosen):
        self.master = master
        self.quiz = quiz
        self.idx = idx
        self.refresh = refresh
        self.master.grab_set()
        self.question = question
        self.on_option_chosen = on_option_chosen
        self.option_labels = []
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    # load widgets on screen
    def load_components(self):
        question_num_label = tk.Label(
            self.frame, text=f"Question {self.idx + 1}", font=("Arial", 18), width=30
        )
        question_num_label.pack()
        if util_data.is_teacher:
            question_var = tk.StringVar()
            question_frame = tk.Frame(self.frame)
            question_label = tk.Label(question_frame, text="Question")
            question_label.pack(side=tk.LEFT)
            question_entry = tk.Entry(question_frame, textvariable=question_var)
            if self.question:
                question_var.set(self.question.question)
            question_entry.pack(side=tk.LEFT, padx=5)
            question_frame.pack(pady=10)

            options_label = tk.Label(self.frame, text="Options")
            options_label.pack(pady=10)
            options_vars = []
            options_frame = tk.Frame(self.frame)
            options_frame.pack()
            for i in range(self.quiz.num_options // 2):
                for j in range(2):
                    option_var = tk.StringVar()
                    options_vars.append(option_var)
                    option_frame = tk.Frame(options_frame)
                    option_label = tk.Label(
                        option_frame, text=str(i * 2 + j + 1), font=("Arial", 16)
                    )
                    option_label.pack(side=tk.LEFT, padx=3)
                    option_entry = tk.Entry(option_frame, textvariable=option_var)
                    if self.question:
                        option_var.set(self.question.options[i * 2 + j])
                    option_entry.pack(side=tk.LEFT, padx=3)
                    option_frame.grid(row=i, column=j, padx=3, pady=3)

            corr_var = tk.IntVar()
            if self.question:
                corr_var.set(self.question.correct_answer_idx + 1)
            corr_frame = tk.Frame(self.frame)
            corr_label = tk.Label(corr_frame, text="Correct Option: ")
            corr_label.pack(side=tk.LEFT, padx=10)
            corr_entry = tk.Entry(corr_frame, textvariable=corr_var)
            corr_entry.pack(side=tk.LEFT)
            corr_frame.pack(pady=10)

            def update_question(*args):
                try:
                    if corr_var.get() > len(options_vars):
                        messagebox.showerror(
                            "Invalid Correct Option", "Chosen option is not available!"
                        )
                        return
                except BaseException as e:
                    print(e)
                    messagebox.showerror("ERROR", str(e))
                    return
                if not self.question:
                    self.question = Question(
                        question=question_var.get(),
                        options=list(map(lambda v: v.get().strip(), options_vars)),
                        quiz_id=self.quiz.id,
                        corr_idx_0=corr_var.get() - 1,
                    )
                else:
                    self.question.question = question_var.get()
                    self.question.options = list(
                        map(lambda v: v.get().strip(), options_vars)
                    )
                    self.question.correct_answer_idx = corr_var.get() - 1
                util_data.quiz_db.update_question(self.question)
                self.master.destroy()
                if self.refresh:
                    self.refresh()

            btn_done = tk.Button(self.frame, text="Done", command=update_question)
            btn_done.pack(pady=15)
        else:
            question_frame = tk.Frame(self.frame)
            question_label = tk.Label(
                question_frame, text=self.question.question, font=("Arial", 16, "bold")
            )
            question_label.pack(side=tk.LEFT)
            question_frame.pack(pady=10)

            options_frame = tk.Frame(self.frame)
            options_frame.pack()

            for i in range(self.quiz.num_options // 2):
                for j in range(2):
                    option_frame = tk.Frame(
                        options_frame,
                        highlightbackground="black",
                        highlightthickness=1,
                        width=20,
                    )
                    option_label = tk.Label(
                        option_frame,
                        text=self.question.options[i * 2 + j],
                        font=("Arial", 16),
                        width=20,
                    )
                    self.option_labels.append(option_label)
                    option_label.pack()
                    option_frame.grid(row=i, column=j, padx=3, pady=3)
                    bind_widgets_in_tag(
                        f"Q{self.question.id}O{i * 2 + j}", option_frame, option_label
                    )

                    def option_chosen(*args, **kwargs):
                        chosen = kwargs["op"]
                        self.on_option_chosen(chosen)
                        for op in self.option_labels:
                            op.configure(bg="#f0f0f0")
                        self.option_labels[chosen].configure(bg="green")

                    option_frame.bind_class(
                        f"Q{self.question.id}O{i * 2 + j}",
                        "<Button>",
                        lambda *args, op=i * 2 + j: option_chosen(op=op),
                    )

            btn_submit = tk.Button(
                self.frame,
                text="SUBMIT",
                font=("Arial", 12),
                command=lambda *args: self.master.destroy(),
            )
            btn_submit.pack(pady=10)
