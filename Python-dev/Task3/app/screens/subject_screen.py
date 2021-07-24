import tkinter as tk

from app.models.subject import Subject
from app.util import util_data


class SubjectScreen:
    def __init__(self, master, refresh):
        self.master = master
        self.refresh = refresh
        self.frame = tk.Frame(self.master)
        self.load_components()
        self.frame.grab_set()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        name_var = tk.StringVar()
        name_frame = tk.Frame(self.frame)
        name_label = tk.Label(name_frame, text="Subject Name: ")
        name_label.pack(side=tk.LEFT)
        name_entry = tk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT)
        name_frame.pack(padx=10)

        def add_subject():
            val = name_var.get().strip()
            if len(val) > 0:
                util_data.quiz_db.add_subject(subject=Subject(name=name_entry.get()))
                self.refresh()
                self.master.destroy()

        btn_frame = tk.Frame(self.frame)
        btn_add = tk.Button(btn_frame, text="Add", command=add_subject)
        btn_add.pack(side=tk.LEFT, padx=10)
        btn_cancel = tk.Button(btn_frame, text="Cancel", command=self.master.destroy)
        btn_cancel.pack(side=tk.RIGHT)
        btn_frame.pack(pady=10)
