import tkinter as tk

from app.util import util_data
from app.widgets.vertical_scrolled_frame import VerticalScrolledFrame


class ScoresScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        # heading
        heading_frame = tk.Frame(self.frame)
        id_label = tk.Label(heading_frame, text="Sl.No.", width=10, anchor=tk.W)
        id_label.pack(side=tk.LEFT, fill=tk.BOTH)
        name_label = tk.Label(heading_frame, text="Name", width=15, anchor=tk.W)
        name_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        regd_num_label = tk.Label(
            heading_frame, text="Regd Number", width=15, anchor=tk.W
        )
        regd_num_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        score_label = tk.Label(heading_frame, text="Score", width=5, anchor=tk.E)
        score_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        heading_frame.pack(pady=10)

        # data
        scores = util_data.score_db.scores()[::-1]
        score_frame = VerticalScrolledFrame(self.frame)
        score_frame.pack()
        for score in scores:
            _ScoreItem(score_frame.interior, score)

        def go_back(*args):
            from .teacher_screen import TeacherScreen

            TeacherScreen(self.master)
            self.frame.destroy()

        btn_back = tk.Button(self.frame, text="Go Back", command=go_back)
        btn_back.pack(pady=10)


class _ScoreItem:
    def __init__(self, master, score):
        self.master = master
        self.score = score
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.pack(padx=3, pady=3)

    def load_components(self):
        id_label = tk.Label(self.frame, text=self.score.id, width=10, anchor=tk.W)
        id_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        name_label = tk.Label(self.frame, text=self.score.name, width=15, anchor=tk.W)
        name_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        regd_num_label = tk.Label(
            self.frame, text=self.score.regd_num, width=15, anchor=tk.W
        )
        regd_num_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        score_label = tk.Label(self.frame, text=self.score.score, width=5, anchor=tk.E)
        score_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
